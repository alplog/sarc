# sarc/agents/task_agent.py

from sarc.protocol.message import SAOMessage, IntentType

class TaskAgent:
    def __init__(self, name="TaskAgent", base_score=65):
        self.name = name
        self.base_score = base_score
        self.capabilities = [IntentType.TASK]

    def can_handle(self, intent: IntentType) -> bool:
        return intent in self.capabilities

    def handle(self, message: SAOMessage) -> str:
        print(f"[{self.name}] Received task:")
        print(f"  Subject: {message.subject}")
        print(f"  Action: {message.action}")
        print(f"  Intent: {message.intent.name}")
        print(f"  Content: {message.content}")

        # Sahte görev simülasyonu
        return f"{self.name} says: Executing task → '{message.content}'... ✅ Done."
