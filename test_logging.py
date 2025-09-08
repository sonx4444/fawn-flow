#!/usr/bin/env python3

import json
from rich.console import Console
from rich.syntax import Syntax

def demo_json_logging():
    """Demonstrate the new JSON logging format."""
    console = Console()
    
    # Sample input data
    input_data = {
        "node": "researcher_agent",
        "status": "started",
        "input": {
            "agent_type": "researcher",
            "step_number": 1,
            "current_task": "Research the basics of artificial intelligence",
            "research_topic": "What is artificial intelligence?",
            "tools_available": [
                {
                    "name": "duckduckgo_search",
                    "description": "A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events."
                }
            ],
            "today": "2024-01-15",
            "previous_observations_count": 0
        }
    }
    
    # Sample output data
    output_data = {
        "node": "researcher_agent",
        "status": "completed",
        "input": input_data["input"],
        "output": {
            "step_completed": 1,
            "reasoning": "I need to search for comprehensive information about artificial intelligence, including its definition, history, and applications.",
            "key_findings": [
                "AI is a branch of computer science that aims to create machines that mimic human intelligence",
                "AI includes machine learning, natural language processing, and computer vision",
                "AI applications span from virtual assistants to autonomous vehicles"
            ],
            "sources": [
                "https://example.com/ai-definition - Comprehensive AI overview",
                "https://example.com/ai-history - History of AI development",
                "https://example.com/ai-applications - Modern AI applications"
            ],
            "final_answer": "Artificial Intelligence (AI) is a comprehensive field focused on creating intelligent machines.",
            "observation_added": True
        }
    }
    
    # Demonstrate the logging format
    console.rule("🚀 RESEARCHER_AGENT - STARTED", style="blue")
    json_str = json.dumps(input_data, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)
    console.print()
    
    console.rule("✅ RESEARCHER_AGENT - COMPLETED", style="green")
    json_str = json.dumps(output_data, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)
    console.print()

if __name__ == "__main__":
    demo_json_logging()
