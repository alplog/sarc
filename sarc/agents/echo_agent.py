# sarc/agents/echo_agent.py

from sarc.protocol.message import SAOMessage, IntentType

class EchoAgent:
    def __init__(self, name="EchoAgent", base_score = 50):
        self.name = name
        self.base_score = base_score
        self.capabilities = [IntentType.GREETING, IntentType.UNKNOWN]

    def can_handle(self, intent: IntentType) -> bool:
        return intent in self.capabilities

    def handle(self, message: SAOMessage) -> str:
        print(f"[{self.name}] Received message:")
        print(f"  Subject: {message.subject}")
        print(f"  Action: {message.action}")
        print(f"  Intent: {message.intent.name}")
        print(f"  Content: {message.content}")
        return f"{self.name} says: You said → '{message.content}'"
