# sarc/protocol/message.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time

class IntentType(Enum):
    TASK = "task"
    QUESTION = "question"
    GREETING = "greeting"
    FEEDBACK = "feedback"
    UNKNOWN = "unknown"

class ErrorType(Enum):
    """Categories of agent processing errors"""
    AGENT_NOT_FOUND = "agent_not_found"
    INTENT_NOT_SUPPORTED = "intent_not_supported"
    PROCESSING_ERROR = "processing_error"
    INVALID_MESSAGE = "invalid_message"
    TIMEOUT = "timeout"
    AUTHENTICATION_ERROR = "authentication_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INTERNAL_ERROR = "internal_error"

@dataclass
class SAOMessage:
    subject: str
    action: str
    object: Optional[str]
    intent: IntentType
    content: str
    metadata: Dict = field (default_factory=lambda: {
        "timestamp": time.time(),
        "lang": "en",
    })

@dataclass
class SAOResponse:
    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None
    error_type: Optional[ErrorType] = None
    agent_id: str = ""
    processing_time: Optional[float] = None
    metadata: Dict = field(default_factory=dict)
    
    @classmethod
    def success_response(cls, data: Any, agent_id: str = "", processing_time: Optional[float] = None) -> 'SAOResponse':
        return cls(
            success=True,
            data=data,
            agent_id=agent_id,
            processing_time=processing_time
        )
    
    @classmethod
    def error_response(cls, error_message: str, error_type: ErrorType, agent_id: str = "", processing_time: Optional[float] = None) -> 'SAOResponse':
        return cls(
            success=False,
            error_message=error_message,
            error_type=error_type,
            agent_id=agent_id,
            processing_time=processing_time
        )

class IntentResolver:
    _mode = "rule-based"

    @classmethod
    def set_mode(cls, mode:str):
        assert mode in ("rule-based", "model"), "Invalid intent resolver mode."
        cls._mode = mode
    
    @staticmethod
    def _rule_based(text: str) -> IntentType:
      lowered = text.lower()

      if any(x in lowered for x in ["do", "make", "create", "summarize", "generate", "run"]):
        return IntentType.TASK

      elif lowered.endswith("?") or any(x in lowered for x in ["how", "what", "why"]):
        return IntentType.QUESTION

      elif any(x in lowered for x in ["hi", "hello", "hey"]):
        return IntentType.GREETING

      elif any(x in lowered for x in ["thanks", "great job", "nice", "feedback"]):
        return IntentType.FEEDBACK

      else:
        return IntentType.UNKNOWN

        
    @staticmethod
    def _model_based(text: str) -> IntentType:
        raise NotImplementedError("Model-based intent resolution not yet implemented.")
    
    @classmethod
    def resolve(cls, text: str) -> IntentType:
        if cls._mode == "rule-based":
            return cls._rule_based(text)
        if cls._mode == "model-based":
            return cls._model_based(text)
