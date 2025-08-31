from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .state import AgentState, create_initial_state
from .agents_mas import search_agent, analysis_agent, database_agent, report_agent
from .communication import communication_manager

def build_mas_graph():
    """Build the multi-agent system workflow using LangGraph"""
    
    # Create the state graph
    workflow = StateGraph(AgentState)
    
    # Add agent nodes
    workflow.add_node("search_agent", search_agent.execute)
    workflow.add_node("analysis_agent", analysis_agent.execute)
    workflow.add_node("database_agent", database_agent.execute)
    workflow.add_node("report_agent", report_agent.execute)
    
    # Define the workflow flow
    workflow.set_entry_point("search_agent")
    
    # Add edges based on agent decisions
    workflow.add_edge("search_agent", "analysis_agent")
    workflow.add_edge("analysis_agent", "database_agent")
    workflow.add_edge("database_agent", "report_agent")
    workflow.add_edge("report_agent", END)
    
    # Compile the graph
    return workflow.compile()

def analyze_page_mas(url: str) -> Dict[str, Any]:
    """Multi-agent system for page analysis"""
    
    # Build the workflow graph
    graph = build_mas_graph()
    
    # Create initial state
    initial_state = create_initial_state(url)
    
    # Execute the workflow
    try:
        final_state = graph.invoke(initial_state)
        
        # Collect results
        result = {
            "success": True,
            "final_report": final_state.get("final_report", ""),
            "agent_log": final_state.get("agent_log", []),
            "errors": final_state.get("errors", []),
            "message_history": communication_manager.get_message_history(),
            "workflow_summary": {
                "total_agents_executed": len(final_state.get("agent_log", [])),
                "final_agent": final_state.get("current_agent", "unknown"),
                "has_errors": len(final_state.get("errors", [])) > 0
            }
        }
        
        return result
        
    except Exception as e:
        # Handle workflow execution errors
        return {
            "success": False,
            "error": str(e),
            "agent_log": initial_state.get("agent_log", []),
            "errors": initial_state.get("errors", []) + [str(e)],
            "message_history": communication_manager.get_message_history()
        }

def get_workflow_status(state: AgentState) -> Dict[str, Any]:
    """Get current workflow status"""
    return {
        "current_agent": state.get("current_agent", "unknown"),
        "next_agent": state.get("next_agent", "unknown"),
        "agents_executed": len(state.get("agent_log", [])),
        "has_content": bool(state.get("extracted_text", "")),
        "has_analysis": bool(state.get("analysis_results", {})),
        "has_database_results": bool(state.get("database_results", {})),
        "has_report": bool(state.get("final_report", "")),
        "errors": state.get("errors", [])
    }
