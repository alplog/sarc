# sarc/core/router.py

from typing import List, Optional
from sarc.protocol.message import SAOMessage, IntentResolver, IntentType

class Agent:
    def __init__(self, name:str, capabilities: List[IntentType], base_score: int = 50):
        self.name = name
        self.capabilities = capabilities
        self.base_score = base_score

    def can_handle(self, intent: IntentType):
        return intent in self.capabilities
    
class Router:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
    def score_confidence(self, agent: Agent, intent: IntentType) -> int :
        if agent.can_handle(intent):
            return agent.base_score + 30
        else:
            return agent.base_score - 50
        
    def route(self, text: str) -> Optional[str]:
        intent = IntentResolver.resolve(text)

        message = SAOMessage(
            subject="user",
            action="auto",
            object=None, 
            intent=intent,
            content=text
        )

        scored = [
            (agent, self.score_confidence(agent, intent))
            for agent in self.agents
        ]

        scored.sort(key=lambda x: x[1], reverse=True)

        top_agent, top_score = scored[0]

        print(f"[Router] Intent {intent.name}, routed to {top_agent.name}, Score: {top_score}")

        if hasattr(top_agent, "handle"):
            response = top_agent.handle(message)
            return response
        else:
            print(f"[Router] Agent {top_agent.name} has no handle() method! ")
            return None
    '''
    To be added:
    -Threshold (Not sending messages to agents below a certain score:)
    -Broadcast Mode (If there is a tie, or no agent supports related intent.)
    '''