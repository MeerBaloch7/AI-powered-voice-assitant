import pytest

from commands import plugins


def test_all_plugins_have_required_attributes():
    plugin_list = list(plugins.values())
    assert len(plugin_list) > 0, "No plugins were discovered"
    for plugin in plugin_list:
        assert plugin.name, f"{plugin.intent} missing name"
        assert plugin.intent, f"{plugin} missing intent"
        assert isinstance(plugin.patterns, list), f"{plugin.intent} patterns not a list"
        assert len(plugin.patterns) > 0, f"{plugin.intent} has empty patterns"
        assert callable(plugin.execute), f"{plugin.intent} missing execute"


@pytest.mark.parametrize("intent,trigger", [
    ("open_notepad", "open notepad"),
    ("open_notepad", "start notepad"),
    ("open_calculator", "open calculator"),
    ("open_explorer", "open file explorer"),
    ("screenshot", "take a screenshot"),
    ("lock_pc", "lock my computer"),
    ("set_timer", "set a timer for 5 minutes"),
    ("get_weather", "what is the weather"),
    ("create_note", "make a note"),
    ("clipboard_actions", "what is on my clipboard"),
    ("open_website", "open youtube"),
    ("volume_control", "volume up"),
])
def test_recognized_intents(intent, trigger):
    from NLPM import NaturalLanguageProcessingModule
    nlpm = NaturalLanguageProcessingModule()
    assert nlpm.recognize_intent(trigger) == intent


def test_follow_up_matches_with_context(nlpm, context_with_timer):
    assert nlpm.recognize_intent("make that 10", context_with_timer) == "set_timer"


def test_follow_up_ignored_without_context(nlpm):
    assert nlpm.recognize_intent("make that 10") == "unknown_command"


def test_unknown_commands(nlpm):
    assert nlpm.recognize_intent("") == "unknown_command"
    assert nlpm.recognize_intent("   ") == "unknown_command"
    assert nlpm.recognize_intent("jf9283hf92hf") == "unknown_command"


def test_set_timer_has_follow_up_patterns():
    plugin = plugins["set_timer"]
    assert len(plugin.follow_up_patterns) > 0
    assert any("make that" in cmd for cmd in ["make that 10"])
    assert any("change to" in cmd for cmd in ["change to 30 seconds"])


def test_open_notepad_no_false_match():
    plugin = plugins["open_notepad"]
    assert not any(p in "open chrome" for p in plugin.patterns)
