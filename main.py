import asyncio
import argparse
from rich.console import Console
from src.config import config

# The new config module handles loading the .env file.
from src.workflow import run_fawn_flow

async def main():
    parser = argparse.ArgumentParser(description="FawnFlow: A simplified, autonomous research agent.")
    parser.add_argument("query", help="The research query.")
    args = parser.parse_args()

    console = Console()
    console.rule(f"{config.LANGCHAIN_PROJECT} — {args.query}")
    await run_fawn_flow(args.query)
    console.rule(f"{config.LANGCHAIN_PROJECT} completed")

if __name__ == "__main__":
    asyncio.run(main())
