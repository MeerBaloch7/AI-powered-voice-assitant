import pytest

from NLPM import NaturalLanguageProcessingModule
from commands import plugins


@pytest.fixture
def nlpm():
    return NaturalLanguageProcessingModule()


def test_all_intents_have_at_least_one_plugin():
    """Every plugin's intent should be discoverable by NLPM."""
    nlpm = NaturalLanguageProcessingModule()
    for intent in plugins:
        plugin = plugins[intent]
        first_pattern = plugin.patterns[0]
        result = nlpm.recognize_intent(first_pattern)
        assert result == intent, f"{first_pattern} should map to {intent}, got {result}"


def test_intent_priority():
    """More specific patterns should match before generic ones."""
    nlpm = NaturalLanguageProcessingModule()
    result = nlpm.recognize_intent("open notepad")
    assert result == "open_notepad"


def test_follow_up_with_context(nlpm):
    from conversation_context import ConversationContext
    ctx = ConversationContext()
    ctx.add_turn("set timer 5 minutes", "set_timer", True, {"duration": 300})
    assert nlpm.recognize_intent("make that 10", ctx) == "set_timer"


def test_follow_up_without_context(nlpm):
    assert nlpm.recognize_intent("make that 10") == "unknown_command"


def test_empty_input(nlpm):
    assert nlpm.recognize_intent("") == "unknown_command"
    assert nlpm.recognize_intent(None) == "unknown_command"


def test_case_insensitive(nlpm):
    assert nlpm.recognize_intent("OPEN NOTEPAD") == "open_notepad"
    assert nlpm.recognize_intent("Open Notepad") == "open_notepad"
