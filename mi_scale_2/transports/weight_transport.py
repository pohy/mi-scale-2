from datetime import datetime
from abc import ABC, abstractmethod

class WeightTransport(ABC):
    @abstractmethod
    def on_measurement(self, weight_kg: float, unit: str, date: datetime):
        pass
