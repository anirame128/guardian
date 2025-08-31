from typing import Dict, List, Any, Optional
from datetime import datetime
from .state import AgentState

class AgentMessage:
    """Represents a message between agents"""
    
    def __init__(self, from_agent: str, to_agent: str, content: Dict[str, Any], message_type: str = "data"):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.message_type = message_type
        self.timestamp = datetime.now().isoformat()
        self.id = f"{from_agent}_{to_agent}_{int(datetime.now().timestamp())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "content": self.content,
            "message_type": self.message_type,
            "timestamp": self.timestamp
        }

class AgentCommunication:
    """Manages inter-agent communication"""
    
    def __init__(self):
        self.message_queue: List[AgentMessage] = []
        self.delivered_messages: List[AgentMessage] = []
    
    def send_message(self, message: AgentMessage) -> str:
        """Send a message between agents"""
        self.message_queue.append(message)
        return message.id
    
    def receive_messages(self, agent: str) -> List[AgentMessage]:
        """Get all messages for a specific agent"""
        messages = [msg for msg in self.message_queue if msg.to_agent == agent]
        # Mark as delivered
        for msg in messages:
            if msg not in self.delivered_messages:
                self.delivered_messages.append(msg)
        return messages
    
    def get_undelivered_messages(self, agent: str) -> List[AgentMessage]:
        """Get undelivered messages for an agent"""
        delivered_ids = [msg.id for msg in self.delivered_messages]
        return [msg for msg in self.message_queue 
                if msg.to_agent == agent and msg.id not in delivered_ids]
    
    def clear_messages(self, agent: str):
        """Clear delivered messages for an agent"""
        self.delivered_messages = [msg for msg in self.delivered_messages if msg.to_agent != agent]
    
    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get complete message history"""
        return [msg.to_dict() for msg in self.message_queue]

# Global communication manager
communication_manager = AgentCommunication()

def send_agent_message(from_agent: str, to_agent: str, content: Dict[str, Any], message_type: str = "data") -> str:
    """Helper function to send messages between agents"""
    message = AgentMessage(from_agent, to_agent, content, message_type)
    return communication_manager.send_message(message)

def receive_agent_messages(agent: str) -> List[AgentMessage]:
    """Helper function to receive messages for an agent"""
    return communication_manager.receive_messages(agent)
