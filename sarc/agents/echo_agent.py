# sarc/agents/echo_agent.py

import time
from sarc.protocol.message import SAOMessage, SAOResponse, IntentType, ErrorType

class EchoAgent:
    def __init__(self, name="EchoAgent", base_score = 50):
        self.name = name
        self.base_score = base_score
        self.capabilities = [IntentType.GREETING, IntentType.UNKNOWN, IntentType.QUESTION]

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
            print(f"[{self.name}] Received message:")
            print(f"  Subject: {message.subject}")
            print(f"  Action: {message.action}")
            print(f"  Intent: {message.intent.name}")
            print(f"  Content: {message.content}")
            
            # Successful response
            response_text = f"{self.name} says: You said → '{message.content}'"
            
            return SAOResponse.success_response(
                data=response_text,
                agent_id=self.name,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            return SAOResponse.error_response(
                error_message=f"Processing error: {str(e)}",
                error_type=ErrorType.PROCESSING_ERROR,
                agent_id=self.name,
                processing_time=time.time() - start_time
            )
