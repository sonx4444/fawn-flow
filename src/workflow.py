
from .graph.builder import build_graph
from .graph.types import FawnState
from rich.console import Console
from rich.markdown import Markdown
from datetime import date

async def run_fawn_flow(query: str):
    graph = build_graph()
    console = Console()
    initial_state: FawnState = {
        "research_topic": query,
        "messages": [("user", query)],
        "observations": [],
        "today": date.today().isoformat(),
    }
    
    # Print the final state. Consider streaming the output.
    final_state: FawnState = await graph.ainvoke(initial_state)

    console.rule("Final Report")
    report = final_state.get("final_report", "No report generated.")
    console.print(Markdown(report if report else "No report generated."))

