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


def test_plugin_exception_is_isolated(cem, monkeypatch):
    plugin = plugins["open_notepad"]
    monkeypatch.setattr(plugin, "execute", lambda command: (_ for _ in ()).throw(RuntimeError("boom")))
    assert cem.execute("open_notepad", "open notepad") is False


def test_previous_data_exposed_to_plugin(cem, context):
    context.add_turn("set timer for 5 minutes", "set_timer", True, {"duration": 300, "unit": "minutes"})
    result = cem.execute("set_timer", "make that 10", context)
    assert result is True
    assert context.last_turn.data["duration"] == 600


def test_failed_plugin_does_not_store_context(cem, context, monkeypatch):
    plugin = plugins["open_notepad"]
    monkeypatch.setattr(plugin, "execute", lambda command: False)
    cem.execute("open_notepad", "open notepad", context)
    assert context.last_turn is None
