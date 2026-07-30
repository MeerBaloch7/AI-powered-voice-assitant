import pytest

from conversation_context import ConversationContext


def test_empty_context():
    ctx = ConversationContext()
    assert ctx.last_turn is None
    assert ctx.last_intent is None
    assert ctx.last_data == {}


def test_add_and_retrieve():
    ctx = ConversationContext()
    ctx.add_turn("hello", "unknown_command", False)
    assert ctx.last_turn is not None
    assert ctx.last_intent == "unknown_command"
    assert ctx.last_data == {}


def test_context_data_stored():
    ctx = ConversationContext()
    ctx.add_turn("set timer 5", "set_timer", True, {"duration": 300})
    assert ctx.last_data == {"duration": 300}


def test_multiple_turns():
    ctx = ConversationContext()
    ctx.add_turn("first", "intent_a", True)
    ctx.add_turn("second", "intent_b", False)
    assert ctx.last_intent == "intent_b"
    assert ctx.last_data == {}


def test_max_turns_eviction():
    ctx = ConversationContext(max_turns=2)
    ctx.add_turn("cmd1", "intent_1", True)
    ctx.add_turn("cmd2", "intent_2", True)
    ctx.add_turn("cmd3", "intent_3", True)
    assert len(ctx._history) == 2
    assert ctx.last_intent == "intent_3"
    assert ctx._history[0].intent == "intent_2"
