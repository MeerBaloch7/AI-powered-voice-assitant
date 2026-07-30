from abc import ABC, abstractmethod


class BasePlugin(ABC):
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

    @abstractmethod
    def execute(self, command: str) -> bool:
        ...
