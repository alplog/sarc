# sarc/protocol/message.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict
import time

class IntentType(Enum):
    TASK = "task"
    QUESTION = "question"
    GREETING = "greeting"
    FEEDBACK = "feedback"
    UNKNOWN = "unknown"

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
