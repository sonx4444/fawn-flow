<div align="center">

# 🦌 FawnFlow

**Your tiny, autonomous research assistant.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by LangChain](https://img.shields.io/badge/powered%20by-LangChain-green?logo=langchain)](https://www.langchain.com/)

</div>

---

An elegant, minimal research agent that plans, searches, executes small code tasks, and produces a clean report — end to end.

FawnFlow is inspired by the excellent (and more feature‑rich) DeerFlow project by ByteDance. If you need a production‑grade, full‑stack deep research system, check out DeerFlow here: [bytedance/deer-flow](https://github.com/bytedance/deer-flow).

## ✨ Key Features

- 🧠 Adaptive planner: small, testable steps; adjusts based on observations
- 🤖 Multi‑agent execution: `researcher` (web), `coder` (Python REPL)
- 🔌 Pluggable search: Tavily, Google, DuckDuckGo
- 📄 Markdown report: clean, readable final output

## Why FawnFlow?

- Small, readable codebase you can understand in one sitting
- Clear LangGraph flow: Planner → Researcher → Coder → Reporter
- Uses a single powerful LLM for planning and reporting

Quick start
-----------
```bash
# PowerShell
$env:OPENAI_API_KEY="..."
# Optional: pick search engine (tavily|google|duckduckgo)
$env:SEARCH_ENGINE="duckduckgo"
# For Google search engine
# $env:GOOGLE_API_KEY="..."; $env:GOOGLE_CSE_ID="..."

uv run python .\main.py "What are the latest approaches to retrieval-augmented generation?"
```

Configuration
-------------
Environment variables (you can also put these in a `.env` file):
- OPENAI_API_KEY (required)
- SEARCH_ENGINE = tavily | google | duckduckgo (default: duckduckgo)
- TAVILY_API_KEY (required if SEARCH_ENGINE=tavily)
- GOOGLE_API_KEY, GOOGLE_CSE_ID (required if SEARCH_ENGINE=google)

Centralized configuration and validation live in `src/config.py`.

Project structure
-----------------
```
.
├─ main.py                 # CLI entry
├─ src/
│  ├─ config.py            # Centralized config
│  ├─ workflow.py          # Orchestrates the run
│  ├─ agents/
│  │  └─ agents.py         # Agent executor factory
│  ├─ graph/
│  │  ├─ builder.py        # LangGraph graph builder
│  │  ├─ nodes.py          # Nodes for planner/researcher/coder/reporter
│  │  ├─ planner_model.py  # Pydantic schemas for plan
│  │  └─ types.py          # State type
│  ├─ tools/
│  │  ├─ search.py         # Search tool with engine selection
│  │  └─ python_repl.py    # Python REPL tool
│  └─ prompts/             # Prompts for each role
└─ docs/                   # Additional documentation (architecture, flow, config, prompts)
```

Docs
----
- `docs/architecture.md` — components and relationships
- `docs/flow.md` — execution flow and streaming notes
- `docs/configuration.md` — environment variables and examples
- `docs/technologies.md` — libraries and services
- `docs/prompts.md` — prompt roles and guidelines

Roadmap
-------
- Event streaming in the terminal (node starts/ends, tool snippets)
- Optional JSON schemas and few‑shot examples for prompts
- Pluggable reporters (Markdown, HTML)

Development
-----------
- Dependencies are managed via `uv` and `pyproject.toml`
- Linting uses Ruff (optional)

License
-------
MIT

