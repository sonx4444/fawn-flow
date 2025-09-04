from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

def create_agent_executor(llm, tools, prompt_template_str: str):
    """Creates a runnable agent executor."""
    prompt = PromptTemplate.from_template(prompt_template_str)
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True for debugging