
from pathlib import Path
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console

from .types import FawnState
from .types import Plan
from ..agents.agents import create_agent_executor
from ..tools.search import search_tool
from ..tools.python_repl import python_repl_tool
from ..config import config

# Initialize the LLM, set a single powerful model for all tasks.
# Validate environment configuration for OpenAI
config.validate_openai()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Simple, shared console for formatted output
console = Console()

# Load prompts from files
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
planner_prompt_template = (PROMPTS_DIR / "planner.md").read_text()
researcher_prompt_template = (PROMPTS_DIR / "researcher.md").read_text()
coder_prompt_template = (PROMPTS_DIR / "coder.md").read_text()
reporter_prompt_template = (PROMPTS_DIR / "reporter.md").read_text()

def coordinator_node(state: FawnState) -> FawnState:
    console.rule("COORDINATOR")
    # Simple pass-through node for now. Can be used for validation or initialization.
    return state

def planner_node(state: FawnState) -> FawnState:
    console.rule("PLANNER")
    
    # Serialize the current plan to a string, or use a default message.
    if state.get("current_plan"):
        plan_str = state["current_plan"].model_dump_json(indent=2)
    else:
        plan_str = "No plan created yet."

    prompt = PromptTemplate.from_template(planner_prompt_template).format(
        research_topic=state["research_topic"],
        plan=plan_str,
        observations="\n".join(state["observations"]),
        today=state.get("today", "")
    )

    # Enforce structured output to Plan; model must return valid JSON matching schema
    structured_llm = llm.with_structured_output(Plan)
    plan: Plan = structured_llm.invoke(prompt)

    state["current_plan"] = plan

    console.print(f" • Thought: {plan.thought}")
    console.print(f" • Decision: {plan.decision}")

    return state

def execute_agent_node(state: FawnState, agent_type: str) -> FawnState:
    console.rule(f"EXECUTING AGENT: {agent_type.upper()}")
    plan = state["current_plan"]
    
    # Find the next pending step for the given agent type
    pending_steps = [s for s in plan.plan if s.status == "pending" and s.agent == agent_type]
    if not pending_steps:
        raise ValueError(f"No pending steps found for agent: {agent_type}")
    step = pending_steps[0]

    # Select tools and prompt based on agent type
    if agent_type == "researcher":
        tools = [search_tool]
        prompt_template = researcher_prompt_template
    elif agent_type == "coder":
        tools = [python_repl_tool]
        prompt_template = coder_prompt_template
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

    agent_executor = create_agent_executor(llm, tools, prompt_template)
    
    # Invoke the agent
    result = agent_executor.invoke({
        "agent_type": agent_type,
        "research_topic": state["research_topic"],
        "current_task": step.task,
        "tools": "\n".join([f'{t.name}: {t.description}' for t in tools]),
        "tool_names": ", ".join([t.name for t in tools]),
        "today": state.get("today", "")
    })

    # Update state with the result
    observation = f"Step {step.step} ({agent_type}): {step.task} -> {result['output']}"
    state["observations"].append(observation)
    
    # Update the status of the completed step
    for s in state["current_plan"].plan:
        if s.step == step.step:
            s.status = "completed"
            break
            
    return state

def researcher_node(state: FawnState) -> FawnState:
    return execute_agent_node(state, "researcher")

def coder_node(state: FawnState) -> FawnState:
    return execute_agent_node(state, "coder")

def reporter_node(state: FawnState) -> FawnState:
    console.rule("REPORTER")
    prompt = PromptTemplate.from_template(reporter_prompt_template).format(
        research_topic=state["research_topic"],
        observations="\n".join(state["observations"]),
        today=state.get("today", "")
    )
    
    response = llm.invoke(prompt)
    
    # Handle empty or invalid responses
    if not response.content or response.content.strip() == "":
        print("Warning: LLM returned empty response, using fallback report")
        state["final_report"] = f"Research Report on: {state['research_topic']}\n\nBased on the observations collected, here is a summary of the research findings."
    else:
        state["final_report"] = response.content
    
    return state