# sarc/core/router.py

from typing import List, Optional
from sarc.protocol.message import SAOMessage, SAOResponse, IntentResolver, IntentType, ErrorType

class Agent:
    def __init__(self, name:str, capabilities: List[IntentType], base_score: int = 50):
        self.name = name
        self.capabilities = capabilities
        self.base_score = base_score

    def can_handle(self, intent: IntentType):
        return intent in self.capabilities
    
class Router:
    def __init__(self, agents: List[Agent], score_threshold: int = 0):
        self.agents = agents
        self.score_threshold = score_threshold
        
    def score_confidence(self, agent: Agent, intent: IntentType) -> int:
        if agent.can_handle(intent):
            return agent.base_score + 30
        else:
            return agent.base_score - 50
        
    def route(self, text: str) -> SAOResponse:
        try:
            # Intent resolution
            intent = IntentResolver.resolve(text)

            # Input validation
            if not text or len(text.strip()) == 0:
                return SAOResponse.error_response(
                    error_message="Message content cannot be empty",
                    error_type=ErrorType.INVALID_MESSAGE,
                    agent_id="Router"
                )

            # Create message
            message = SAOMessage(
                subject="user",
                action="auto",
                object=None, 
                intent=intent,
                content=text
            )

            # Score agents
            scored = [
                (agent, self.score_confidence(agent, intent))
                for agent in self.agents
            ]

            scored.sort(key=lambda x: x[1], reverse=True)

            # Get highest scoring agent
            if not scored:
                return SAOResponse.error_response(
                    error_message="No agents found",
                    error_type=ErrorType.AGENT_NOT_FOUND,
                    agent_id="Router"
                )

            top_agent, top_score = scored[0]

            # Threshold check
            if top_score < self.score_threshold:
                return SAOResponse.error_response(
                    error_message=f"Highest score ({top_score}) is below threshold ({self.score_threshold})",
                    error_type=ErrorType.INTENT_NOT_SUPPORTED,
                    agent_id="Router"
                )

            print(f"[Router] Intent {intent.name}, routed to {top_agent.name}, Score: {top_score}")

            # Send message to agent
            if hasattr(top_agent, "handle"):
                response = top_agent.handle(message)
                
                # If agent returns SAOResponse, return directly
                if isinstance(response, SAOResponse):
                    return response
                
                # Convert legacy string responses to SAOResponse
                return SAOResponse.success_response(
                    data=response,
                    agent_id=top_agent.name
                )
            else:
                return SAOResponse.error_response(
                    error_message=f"Agent {top_agent.name} does not have handle() method",
                    error_type=ErrorType.PROCESSING_ERROR,
                    agent_id="Router"
                )
                
        except Exception as e:
            return SAOResponse.error_response(
                error_message=f"Router error: {str(e)}",
                error_type=ErrorType.INTERNAL_ERROR,
                agent_id="Router"
            )
    
    '''
    Future features:
    -Broadcast Mode (If there is a tie, or no agent supports related intent.)
    -Agent health checking
    -Load balancing
    '''