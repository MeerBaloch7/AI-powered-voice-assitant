import sys

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
    assert any(p in "make that 10" for p in plugin.follow_up_patterns)
    assert any(p in "change to 30 seconds" for p in plugin.follow_up_patterns)


def test_open_notepad_no_false_match():
    plugin = plugins["open_notepad"]
    assert not any(p in "open chrome" for p in plugin.patterns)


def test_volume_unmute_does_not_mute(monkeypatch, mocker):
    import commands.volume_control as vc_mod
    monkeypatch.setattr(vc_mod.os, "name", "nt")
    plugin = plugins["volume_control"]
    fake_volume = mocker.Mock()
    monkeypatch.setattr(plugin, "_get_volume_interface", lambda: fake_volume)

    assert plugin.execute("unmute") is True
    fake_volume.SetMute.assert_called_once_with(0, None)


def test_volume_mute(monkeypatch, mocker):
    import commands.volume_control as vc_mod
    monkeypatch.setattr(vc_mod.os, "name", "nt")
    plugin = plugins["volume_control"]
    fake_volume = mocker.Mock()
    monkeypatch.setattr(plugin, "_get_volume_interface", lambda: fake_volume)

    assert plugin.execute("mute the volume") is True
    fake_volume.SetMute.assert_called_once_with(1, None)


def test_volume_percentage(monkeypatch, mocker):
    import commands.volume_control as vc_mod
    monkeypatch.setattr(vc_mod.os, "name", "nt")
    plugin = plugins["volume_control"]
    fake_volume = mocker.Mock()
    monkeypatch.setattr(plugin, "_get_volume_interface", lambda: fake_volume)

    assert plugin.execute("set volume to 50") is True
    fake_volume.SetMasterVolumeLevelScalar.assert_called_once_with(0.5, None)


def test_volume_pycaw_failure_returns_false(monkeypatch, mocker):
    import commands.volume_control as vc_mod
    monkeypatch.setattr(vc_mod.os, "name", "nt")
    plugin = plugins["volume_control"]
    monkeypatch.setattr(plugin, "_get_volume_interface", mocker.Mock(side_effect=RuntimeError("no speakers")))

    assert plugin.execute("mute") is False


def test_search_google_url_encoding(mocker):
    plugin = plugins["search_google"]
    mock_open = mocker.patch("webbrowser.open")

    assert plugin.execute("search google for a & b ?") is True
    url = mock_open.call_args.args[0]
    assert "q=a+%26+b+%3F" in url


def test_search_google_strips_trigger(mocker):
    plugin = plugins["search_google"]
    mock_open = mocker.patch("webbrowser.open")

    assert plugin.execute("look up the weather in London") is True
    url = mock_open.call_args.args[0]
    assert "q=weather+in+London" in url


def test_weather_city_encoded(mocker):
    plugin = plugins["get_weather"]
    fake_response = mocker.Mock(status_code=200, text="Clear, 20C")
    mock_get = mocker.patch("requests.get", return_value=fake_response)

    assert plugin.execute("what is the weather in new york") is True
    url = mock_get.call_args.args[0]
    assert "new+york" in url


def test_weather_request_failure_returns_false(mocker):
    import requests
    plugin = plugins["get_weather"]
    mocker.patch("requests.get", side_effect=requests.RequestException("timeout"))

    assert plugin.execute("weather") is False


def test_screenshot_save_failure_returns_false(monkeypatch, mocker):
    fake_pyautogui = mocker.Mock()
    fake_pyautogui.screenshot.side_effect = OSError("permission denied")
    monkeypatch.setitem(sys.modules, "pyautogui", fake_pyautogui)

    plugin = plugins["screenshot"]
    assert plugin.execute("take screenshot") is False
