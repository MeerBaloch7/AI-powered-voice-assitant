from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationTurn:
    command: str
    intent: str
    success: bool
    data: dict[str, Any] = field(default_factory=dict)


class ConversationContext:
    def __init__(self, max_turns: int = 5):
        self._history: deque[ConversationTurn] = deque(maxlen=max_turns)

    def add_turn(self, command: str, intent: str, success: bool, data: dict | None = None):
        self._history.append(ConversationTurn(command, intent, success, data or {}))

    @property
    def last_turn(self) -> ConversationTurn | None:
        return self._history[-1] if self._history else None

    @property
    def last_intent(self) -> str | None:
        turn = self.last_turn
        return turn.intent if turn else None

    @property
    def last_data(self) -> dict[str, Any]:
        turn = self.last_turn
        return turn.data if turn else {}
