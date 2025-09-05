<div align="center">

# 🦌 FawnFlow

**Your tiny, autonomous research assistant.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by LangChain](https://img.shields.io/badge/powered%20by-LangChain-green?logo=langchain)](https://www.langchain.com/)

</div>

---

FawnFlow is an elegant, minimal research agent that plans, searches, executes small code tasks, and produces a clean report — end to end. It is designed to be a small, readable codebase that you can understand in one sitting.

It is inspired by the excellent (and more feature‑rich) [DeerFlow project by ByteDance](https://github.com/bytedance/deer-flow).

## 🛠️ How It Works

FawnFlow operates on a clear, stateful loop powered by LangGraph. The agent's lifecycle is a cycle of planning, execution, and observation.

<div align="center">
  <img src="./docs/flow-diagram.svg" alt="FawnFlow Workflow Diagram" width="720">
</div>

1.  **Plan:** The **Planner** reviews the research goal, observations, and its own previous steps to create or revise a multi-step plan.
2.  **Execute:** The next pending step is executed by the appropriate agent (`researcher` or `coder`), which performs its task and returns the results.
3.  **Report:** Once the planner decides the research is complete, the **Reporter** synthesizes all observations and raw data into a final Markdown report.

## ✨ Key Features

- 🧠 **Stateful Planner**: Maintains and revises a persistent, multi-step plan.
- 📝 **Enriched Context**: Retains raw tool outputs for high-fidelity, detailed reporting.
- 🤖 **Multi-Agent Execution**: Utilizes a `researcher` for web searches and a `coder` for running Python code.
- 🔌 **Pluggable Search**: Easily switch between Tavily, Google, Brave, and DuckDuckGo.
- 📄 **Markdown Reports**: Generates clean, readable final reports.

## 🚀 Quick Start

```bash
# PowerShell
$env:OPENAI_API_KEY="..."
# Optional: pick search engine (tavily|google|brave|duckduckgo)
$env:SEARCH_ENGINE="duckduckgo"
# For Google search engine
# $env:GOOGLE_API_KEY="..."; $env:GOOGLE_CSE_ID="..."

uv run python .\main.py "What are the latest approaches to retrieval-augmented generation?"
```

## ⚙️ Configuration

Configuration is handled via environment variables. You can also place these in a `.env` file in the project root.

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | **Required.** Your OpenAI API key. | (none) |
| `SEARCH_ENGINE` | The search engine to use. | `duckduckgo` |
| `TAVILY_API_KEY` | Required if `SEARCH_ENGINE=tavily`. | (none) |
| `GOOGLE_API_KEY` | Required if `SEARCH_ENGINE=google`. | (none) |
| `GOOGLE_CSE_ID` | Required if `SEARCH_ENGINE=google`. | (none) |
| `BRAVE_SEARCH_API_KEY` | Required if `SEARCH_ENGINE=brave`. | (none) |

Centralized configuration and validation live in `src/config.py`.

## 📂 Project Structure

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
│  │  └─ types.py          # Pydantic schemas for plan and state type
│  ├─ tools/
│  │  ├─ search.py         # Search tool with engine selection
│  │  └─ python_repl.py    # Python REPL tool
│  └─ prompts/             # Prompts for each role
└─ docs/                   # Additional documentation
```

## 📚 Docs

- `docs/architecture.md` — components and relationships
- `docs/flow.md` — execution flow and streaming notes
- `docs/configuration.md` — environment variables and examples
- `docs/technologies.md` — libraries and services
- `docs/prompts.md` — prompt roles and guidelines

## 🗺️ Roadmap

- Event streaming in the terminal (node starts/ends, tool snippets)
- Optional JSON schemas and few‑shot examples for prompts
- Pluggable reporters (Markdown, HTML)

## 💻 Development

- Dependencies are managed via `uv` and `pyproject.toml`.
- Linting uses Ruff (optional).

## 📄 License

MIT

