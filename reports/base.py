from abc import ABC, abstractmethod
from typing import DefaultDict


class Report(ABC):
    name: str

    @abstractmethod
    def generate(
        self,
        data: DefaultDict[str, DefaultDict[str, int]],
        total: int
    ) -> str:
        """
        Должен возвращать готовый текст отчёта.
        """
        pass
