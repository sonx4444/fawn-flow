Architecture
============

Overview
--------
FawnFlow is a small LangGraph-driven agent with four roles: Planner, Researcher, Coder, and Reporter. It uses a central `FawnState` carried through nodes to coordinate actions.

Core components
---------------
- Graph (LangGraph): orchestrates node execution and state flow
- Nodes: functions in `src/graph/nodes.py` (planner, researcher, coder, reporter)
- Tools: `search.py` (Tavily/Google/DDG) and `python_repl.py`
- LLM: OpenAI via `ChatOpenAI` used for planning and reporting
- Config: `src/config.py` centralizes environment and validations

State model
-----------
- `research_topic: str`
- `messages: list[(role, content)]` (from LangGraph `MessagesState`)
- `observations: list[str]`
- `current_plan: Plan | None`
- `final_report: str`

Data flow
---------
1. Planner creates a structured `Plan` (Pydantic model)
2. Researcher executes steps using `search_tool`, appending `observations`
3. Coder optionally executes Python tasks
4. Reporter compiles `final_report` from `observations`

Extensibility
-------------
- Swap search engine via `SEARCH_ENGINE`
- Add nodes by extending the builder and state transitions
- Add tools by creating LangChain Tool wrappers


