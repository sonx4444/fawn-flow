from langgraph.graph import StateGraph, END, START
from .types import FawnState
from .nodes import (
    coordinator_node,
    planner_node,
    researcher_node,
    coder_node,
    reporter_node,
)

def should_continue(state: FawnState) -> str:
    """Determines the next step based on the planner's decision."""
    if state["current_plan"].decision == "FINISH":
        return "reporter"
    
    # Find the next pending step
    pending_steps = [s for s in state["current_plan"].plan if s.status == "pending"]
    if not pending_steps:
        # This case should ideally not be reached if the planner decides to CONTINUE
        return "reporter"
    
    # Check if we have enough observations to make a decision
    if len(state["observations"]) >= 5:  # Limit to prevent infinite loops
        return "reporter"
        
    next_agent = pending_steps[0].agent
    return next_agent # "researcher" or "coder"

def build_graph():
    """Builds the FawnFlow graph."""
    builder = StateGraph(FawnState)

    # Add nodes
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("coder", coder_node)
    builder.add_node("reporter", reporter_node)

    # Define the workflow edges
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "planner")
    
    # The core loop: after executing a step, always go back to the planner to re-assess
    builder.add_edge("researcher", "planner")
    builder.add_edge("coder", "planner")

    # The planner is the central router
    builder.add_conditional_edges(
        "planner",
        should_continue,
        {
            "reporter": "reporter", # If the planner decides to FINISH, go to reporter.
            "researcher": "researcher",
            "coder": "coder",
        },
    )
    
    # The reporter node is the last step before the end
    builder.add_edge("reporter", END)

    # Compile and return the graph
    return builder.compile()