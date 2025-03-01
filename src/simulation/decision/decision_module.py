from abc import ABC, abstractmethod
from typing import Dict, Any
from mesa import Agent


class DecisionModule(ABC):

    @abstractmethod
    def decide_next_action(self, agent: Agent) -> Dict[str, Any]:
        pass