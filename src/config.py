import os
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Centralized configuration singleton loaded from environment/.env."""

    def __init__(self) -> None:
        load_dotenv()

        self.OPENAI_API_KEY: Optional[str] = self._get("OPENAI_API_KEY")
        self.TAVILY_API_KEY: Optional[str] = self._get("TAVILY_API_KEY")
        self.GOOGLE_API_KEY: Optional[str] = self._get("GOOGLE_API_KEY")
        self.GOOGLE_CSE_ID: Optional[str] = self._get("GOOGLE_CSE_ID")
        self.BRAVE_SEARCH_API_KEY: Optional[str] = self._get("BRAVE_SEARCH_API_KEY")
        self.SEARCH_ENGINE: str = self._get("SEARCH_ENGINE", "duckduckgo").lower()
        self.LANGCHAIN_PROJECT: str = self._get("LANGCHAIN_PROJECT", "FawnFlow")

    def _get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        value = os.getenv(name, default)
        if value is None:
            return None
        return value.strip()

    def require(self, name: str) -> str:
        value = self._get(name)
        if not value:
            raise EnvironmentError(
                f"{name} is not set. Please set it in your environment or .env file."
            )
        return value

    def is_truthy(self, name: str, default: bool = False) -> bool:
        value = self._get(name)
        if value is None:
            return default
        return value.lower() in {"1", "true", "yes", "on"}

    def validate_openai(self) -> None:
        self.require("OPENAI_API_KEY")

    def validate_tavily(self) -> None:
        self.require("TAVILY_API_KEY")

    def validate_google_search(self) -> None:
        self.require("GOOGLE_API_KEY")
        self.require("GOOGLE_CSE_ID")

    def validate_brave_search(self) -> None:
        self.require("BRAVE_SEARCH_API_KEY")


config = Config()
