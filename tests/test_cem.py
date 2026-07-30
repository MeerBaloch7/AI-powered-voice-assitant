import pytest

from commands import plugins
from CEM import CommandExecutionModule
from conversation_context import ConversationContext


@pytest.fixture
def cem():
    return CommandExecutionModule()


@pytest.fixture
def context():
    return ConversationContext()


def test_dispatch_known_intent(cem):
    assert cem.execute("open_notepad", "open notepad") is True


def test_dispatch_unknown_intent(cem):
    assert cem.execute("nonexistent_intent", "whatever") is False


def test_dispatch_empty_intent(cem):
    assert cem.execute("") is False


def test_cem_stores_context_data(cem, context):
    result = cem.execute("set_timer", "set timer for 5 minutes", context)
    assert result is True
    turn = context.last_turn
    assert turn is not None
    assert turn.intent == "set_timer"
    assert "duration" in turn.data


def test_unknown_intent_not_stored_in_context(cem, context):
    cem.execute("nonexistent", "blah", context)
    assert context.last_turn is None
