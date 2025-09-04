Prompts
=======

Files
-----
- `planner.md` — creates a structured Plan
- `researcher.md` — uses the search tool to gather evidence
- `coder.md` — performs small Python tasks
- `reporter.md` — compiles the final Markdown report

Guidelines
---------
- Keep inputs consistent: `research_topic`, `observations`, `current_task`, `tools`, `tool_names`
- Favor concise outputs; avoid repetition
- Cite credible sources in research; prefer unique domains
- Reporter should ground claims in cited sources

Future enhancements
-------------------
- Add JSON schemas for structured outputs
- Add few-shot examples per role (tiny, focused)
- Add a self-checklist to reduce errors


