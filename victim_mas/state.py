from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class AgentState(TypedDict):
    """Shared state structure for the multi-agent system"""
    # Input
    url: str
    
    # Agent outputs
    html_content: str
    extracted_text: str
    analysis_results: Dict[str, Any]
    database_results: Dict[str, Any]
    final_report: str
    
    # Workflow control
    current_agent: str
    next_agent: Optional[str]
    
    # Monitoring
    errors: List[str]
    agent_log: List[Dict[str, Any]]
    
    # Communication
    messages: List[Dict[str, Any]]
    
    # Timestamps
    created_at: str
    last_updated: str

def create_initial_state(url: str) -> AgentState:
    """Create initial state for the multi-agent workflow"""
    return {
        "url": url,
        "html_content": "",
        "extracted_text": "",
        "analysis_results": {},
        "database_results": {},
        "final_report": "",
        "current_agent": "search_agent",
        "next_agent": None,
        "errors": [],
        "agent_log": [],
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }

def update_state_timestamp(state: AgentState) -> AgentState:
    """Update the last_updated timestamp"""
    return {**state, "last_updated": datetime.now().isoformat()}
