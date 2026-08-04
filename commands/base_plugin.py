from abc import ABC, abstractmethod


class BasePlugin(ABC):
    def __init__(self):
        self.context_data: dict = {}
        self.previous_data: dict = {}

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def intent(self) -> str:
        ...

    @property
    @abstractmethod
    def patterns(self) -> list[str]:
        ...

    @property
    def follow_up_patterns(self) -> list[str]:
        return []

    @abstractmethod
    def execute(self, command: str) -> bool:
        ...
