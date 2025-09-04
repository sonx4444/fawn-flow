from ..config import config

SEARCH_ENGINE = config.SEARCH_ENGINE

if SEARCH_ENGINE == "tavily":
    from langchain_tavily import TavilySearch
    config.validate_tavily()
    search_tool = TavilySearch(max_results=3)

elif SEARCH_ENGINE == "google":
    # Uses Google Programmable Search Engine (CSE)
    # Required env vars: GOOGLE_API_KEY, GOOGLE_CSE_ID
    from langchain_community.utilities import GoogleSearchAPIWrapper
    from langchain_community.tools.google_search.tool import GoogleSearchRun

    config.validate_google_search()
    api_wrapper = GoogleSearchAPIWrapper()
    search_tool = GoogleSearchRun(api_wrapper=api_wrapper)

elif SEARCH_ENGINE in ("duckduckgo", "ddg"):
    # DuckDuckGo requires no API key
    from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

    search_tool = DuckDuckGoSearchRun()

else:
    raise ValueError(
        "Unsupported SEARCH_ENGINE. Use one of: tavily, google, duckduckgo"
    )