from typing import List, Literal, Optional
from pydantic import BaseModel
from typing import List, Literal, Optional
from langgraph.graph import MessagesState

class PlanStep(BaseModel):
    """A single step in the research plan."""
    step: int
    task: str
    agent: Literal["researcher", "coder"]
    status: Literal["pending", "completed", "failed"] = "pending"

class Plan(BaseModel):
    """The overall research plan."""
    thought: str
    decision: Literal["CONTINUE", "FINISH"]
    plan: List[PlanStep]


class ResearchResult(BaseModel):
    """Structured output for researcher agent."""
    reasoning: str
    key_findings: List[str]
    sources: List[str]
    final_answer: str

class CodingResult(BaseModel):
    """Structured output for coder agent."""
    reasoning: str
    code_executed: str
    execution_output: str
    final_answer: str

class ReportResult(BaseModel):
    """Structured output for reporter."""
    final_report: str

class FawnState(MessagesState):
    """Represents the state of the FawnFlow workflow."""
    
    research_topic: str = ""
    today: str = ""
    observations: List[str] = []
    current_plan: Optional[Plan] = None
    final_report: str = ""
