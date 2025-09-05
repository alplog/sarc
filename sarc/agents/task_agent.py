# sarc/agents/task_agent.py

import time
from sarc.protocol.message import SAOMessage, SAOResponse, IntentType, ErrorType

class TaskAgent:
    def __init__(self, name="TaskAgent", base_score=65):
        self.name = name
        self.base_score = base_score
        self.capabilities = [IntentType.TASK]

    def can_handle(self, intent: IntentType) -> bool:
        return intent in self.capabilities

    def handle(self, message: SAOMessage) -> SAOResponse:
        start_time = time.time()
        
        try:
            # Intent validation
            if not self.can_handle(message.intent):
                return SAOResponse.error_response(
                    error_message=f"Intent '{message.intent.name}' is not supported",
                    error_type=ErrorType.INTENT_NOT_SUPPORTED,
                    agent_id=self.name,
                    processing_time=time.time() - start_time
                )
            
            # Print debug information
            print(f"[{self.name}] Received task:")
            print(f"  Subject: {message.subject}")
            print(f"  Action: {message.action}")
            print(f"  Intent: {message.intent.name}")
            print(f"  Content: {message.content}")

            # Simple task validation
            if not message.content or len(message.content.strip()) == 0:
                return SAOResponse.error_response(
                    error_message="Task content cannot be empty",
                    error_type=ErrorType.INVALID_MESSAGE,
                    agent_id=self.name,
                    processing_time=time.time() - start_time
                )

            # Mock task simulation
            response_text = f"{self.name} says: Executing task → '{message.content}'... ✅ Done."
            
            return SAOResponse.success_response(
                data=response_text,
                agent_id=self.name,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            return SAOResponse.error_response(
                error_message=f"Task processing error: {str(e)}",
                error_type=ErrorType.PROCESSING_ERROR,
                agent_id=self.name,
                processing_time=time.time() - start_time
            )
