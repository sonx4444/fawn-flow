Configuration
=============

Environment variables
---------------------
- `OPENAI_API_KEY` (required)
- `SEARCH_ENGINE` = `tavily` | `google` | `duckduckgo` (default: `duckduckgo`)
- `TAVILY_API_KEY` (required if `SEARCH_ENGINE=tavily`)
- `GOOGLE_API_KEY`, `GOOGLE_CSE_ID` (required if `SEARCH_ENGINE=google`)

How it works
------------
`src/config.py` loads `.env`, exposes attributes via a singleton `config`, and provides validation helpers.

Example
-------
```python
from src.config import config

config.validate_openai()
if config.SEARCH_ENGINE == "google":
    config.validate_google_search()
```


