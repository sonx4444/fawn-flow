Flow
====

High-level
----------
1. User starts the app via CLI (`main.py`)
2. `workflow.run_fawn_flow` builds the graph and invokes it
3. `nodes.planner_node` creates a Plan
4. Execution alternates between Researcher and Coder steps
5. `nodes.reporter_node` produces the final Markdown report

Events and streaming
--------------------
This scaffold prints section headers and a final Markdown-rendered report. You can adopt LangGraph `astream_events` for live updates per node.

Error handling
--------------
- Missing API keys are validated by `config`
- Empty model responses fallback to a basic report


