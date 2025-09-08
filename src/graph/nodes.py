
from pathlib import Path
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.syntax import Syntax

from .types import FawnState
from .types import Plan, ResearchResult, CodingResult, ReportResult
from ..tools.search import search_tool
from ..tools.python_repl import python_repl_tool
from ..config import config

# Initialize the LLM, set a single powerful model for all tasks.
# Validate environment configuration for OpenAI
config.validate_openai()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Simple, shared console for formatted output
console = Console()

def log_node_execution(node_name: str, input_data: dict, output_data: dict = None, status: str = "started"):
    """Log node execution with consistent JSON formatting."""
    log_data = {
        "node": node_name,
        "status": status,
        "input": input_data
    }
    
    if output_data is not None:
        log_data["output"] = output_data
    
    # Pretty print JSON with syntax highlighting
    json_str = json.dumps(log_data, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    
    if status == "started":
        console.rule(f"🚀 {node_name.upper()} - STARTED", style="blue")
    elif status == "completed":
        console.rule(f"✅ {node_name.upper()} - COMPLETED", style="green")
    elif status == "failed":
        console.rule(f"❌ {node_name.upper()} - FAILED", style="red")
    
    console.print(syntax)
    console.print()

# Load prompts from files
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
planner_prompt_template = (PROMPTS_DIR / "planner.md").read_text()
researcher_prompt_template = (PROMPTS_DIR / "researcher.md").read_text()
coder_prompt_template = (PROMPTS_DIR / "coder.md").read_text()
reporter_prompt_template = (PROMPTS_DIR / "reporter.md").read_text()

def coordinator_node(state: FawnState) -> FawnState:
    input_data = {
        "research_topic": state["research_topic"],
        "today": state.get("today", ""),
        "messages_count": len(state.get("messages", [])),
        "observations_count": len(state.get("observations", []))
    }
    
    log_node_execution("coordinator", input_data, status="started")
    
    # Simple pass-through node for now. Can be used for validation or initialization.
    output_data = {
        "action": "pass_through",
        "state_unchanged": True
    }
    
    log_node_execution("coordinator", input_data, output_data, status="completed")
    return state

def planner_node(state: FawnState) -> FawnState:
    # Serialize the current plan to a string, or use a default message.
    if state.get("current_plan"):
        plan_str = state["current_plan"].model_dump_json(indent=2)
    else:
        plan_str = "No plan created yet."

    input_data = {
        "research_topic": state["research_topic"],
        "today": state.get("today", ""),
        "current_plan": plan_str,
        "observations_count": len(state["observations"]),
        "observations": state["observations"] if len(state["observations"]) <= 3 else state["observations"][-3:]  # Show last 3 for brevity
    }
    
    log_node_execution("planner", input_data, status="started")

    prompt = PromptTemplate.from_template(planner_prompt_template).format(
        research_topic=state["research_topic"],
        plan=plan_str,
        observations="\n".join(state["observations"]),
        today=state.get("today", "")
    )

    try:
        # Enforce structured output to Plan; model must return valid JSON matching schema
        structured_llm = llm.with_structured_output(Plan)
        plan: Plan = structured_llm.invoke(prompt)

        state["current_plan"] = plan

        output_data = {
            "thought": plan.thought,
            "decision": plan.decision,
            "plan_steps": [
                {
                    "step": step.step,
                    "task": step.task,
                    "agent": step.agent,
                    "status": step.status
                } for step in plan.plan
            ]
        }
        
        log_node_execution("planner", input_data, output_data, status="completed")

    except Exception as e:
        error_output = {
            "error": str(e),
            "fallback_action": "using_previous_plan_or_default"
        }
        log_node_execution("planner", input_data, error_output, status="failed")
        raise

    return state

def execute_agent_node(state: FawnState, agent_type: str) -> FawnState:
    plan = state["current_plan"]
    
    # Find the next pending step for the given agent type
    pending_steps = [s for s in plan.plan if s.status == "pending" and s.agent == agent_type]
    if not pending_steps:
        raise ValueError(f"No pending steps found for agent: {agent_type}")
    step = pending_steps[0]

    # Select structured output model, tools, and prompt based on agent type
    if agent_type == "researcher":
        structured_llm = llm.with_structured_output(ResearchResult)
        tools = [search_tool]
        prompt_template = researcher_prompt_template
    elif agent_type == "coder":
        structured_llm = llm.with_structured_output(CodingResult)
        tools = [python_repl_tool]
        prompt_template = coder_prompt_template
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

    # Prepare input data for logging
    input_data = {
        "agent_type": agent_type,
        "step_number": step.step,
        "current_task": step.task,
        "research_topic": state["research_topic"],
        "tools_available": [{"name": t.name, "description": t.description} for t in tools],
        "today": state.get("today", ""),
        "previous_observations_count": len(state["observations"])
    }
    
    log_node_execution(f"{agent_type}_agent", input_data, status="started")

    # Create the prompt
    prompt = PromptTemplate.from_template(prompt_template).format(
        research_topic=state["research_topic"],
        current_task=step.task,
        tools="\n".join([f'{t.name}: {t.description}' for t in tools]),
        today=state.get("today", "")
    )
    
    # Get structured result
    try:
        result = structured_llm.invoke(prompt)
        
        # Create detailed observation based on agent type
        if agent_type == "researcher":
            detailed_obs = f"""Step {step.step} ({agent_type}): {step.task}

Reasoning: {result.reasoning}

Key Findings:
{chr(10).join([f"• {finding}" for finding in result.key_findings])}

Sources:
{chr(10).join([f"• {source}" for source in result.sources])}

Result: {result.final_answer}"""
            
            output_data = {
                "step_completed": step.step,
                "reasoning": result.reasoning,
                "key_findings": result.key_findings,
                "sources": result.sources,
                "final_answer": result.final_answer,
                "observation_added": True
            }
        else:  # coder
            detailed_obs = f"""Step {step.step} ({agent_type}): {step.task}

Reasoning: {result.reasoning}

Code Executed:
```python
{result.code_executed}
```

Execution Output:
```
{result.execution_output}
```

Result: {result.final_answer}"""
            
            output_data = {
                "step_completed": step.step,
                "reasoning": result.reasoning,
                "code_executed": result.code_executed,
                "execution_output": result.execution_output,
                "final_answer": result.final_answer,
                "observation_added": True
            }
            
        state["observations"].append(detailed_obs)
        
        # Update the status of the completed step
        for s in state["current_plan"].plan:
            if s.step == step.step:
                s.status = "completed"
                break
        
        log_node_execution(f"{agent_type}_agent", input_data, output_data, status="completed")
        
    except Exception as e:
        # Fallback observation
        error_obs = f"Step {step.step} ({agent_type}): {step.task} -> Error: {str(e)}"
        state["observations"].append(error_obs)
        
        # Mark step as failed
        for s in state["current_plan"].plan:
            if s.step == step.step:
                s.status = "failed"
                break
        
        error_output = {
            "step_failed": step.step,
            "error": str(e),
            "error_observation_added": True,
            "step_status": "failed"
        }
        
        log_node_execution(f"{agent_type}_agent", input_data, error_output, status="failed")
        return state
            
    return state

def researcher_node(state: FawnState) -> FawnState:
    return execute_agent_node(state, "researcher")

def coder_node(state: FawnState) -> FawnState:
    return execute_agent_node(state, "coder")

def reporter_node(state: FawnState) -> FawnState:
    input_data = {
        "research_topic": state["research_topic"],
        "today": state.get("today", ""),
        "observations_count": len(state["observations"]),
        "observations_summary": [obs[:100] + "..." if len(obs) > 100 else obs for obs in state["observations"][:3]]  # First 3 observations, truncated
    }
    
    log_node_execution("reporter", input_data, status="started")
    
    structured_llm = llm.with_structured_output(ReportResult)
    prompt = PromptTemplate.from_template(reporter_prompt_template).format(
        research_topic=state["research_topic"],
        observations="\n".join(state["observations"]),
        today=state.get("today", "")
    )
    
    try:
        result = structured_llm.invoke(prompt)
        state["final_report"] = result.final_report
        
        output_data = {
            "report_generated": True,
            "report_length": len(result.final_report),
            "report_preview": result.final_report[:200] + "..." if len(result.final_report) > 200 else result.final_report
        }
        
        log_node_execution("reporter", input_data, output_data, status="completed")
        
    except Exception as e:
        # Fallback report
        fallback_report = f"""# Research Report: {state['research_topic']}

*Generated on {state.get('today', 'Unknown Date')}*

## Summary

Based on the observations collected during the research process, here is a summary of the findings:

## Observations

{chr(10).join([f"### {i+1}. Observation\n{obs}\n" for i, obs in enumerate(state['observations'])])}

## Conclusion

The research process encountered an error during report generation. The above observations represent the raw data collected during the investigation."""
        
        state["final_report"] = fallback_report
        
        error_output = {
            "error": str(e),
            "fallback_report_generated": True,
            "fallback_report_length": len(fallback_report)
        }
        
        log_node_execution("reporter", input_data, error_output, status="failed")
    
    return state