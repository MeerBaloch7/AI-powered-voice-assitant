from .base_plugin import BasePlugin


class GetWeatherPlugin(BasePlugin):
    name = "Get Weather"
    intent = "get_weather"
    patterns = [
        "weather", "what is the weather", "what's the weather",
        "weather today", "weather report", "temperature",
        "how is the weather", "forecast",
    ]

    def execute(self, command: str) -> bool:
        try:
            import requests

            # Try to extract a city name from the command
            cmd = command.lower()
            city = None
            for word in ["in ", "at ", "for "]:
                if word in cmd:
                    parts = cmd.split(word, 1)
                    if len(parts) > 1 and parts[1].strip():
                        city = parts[1].strip()
                        break

            if city:
                url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
            else:
                url = "https://wttr.in/?format=%C+%t+%w+%h"

            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Weather info: {response.text.strip()}")
                return True

            print("Could not fetch weather information.")
            return False
        except ImportError:
            print("requests is not installed. Run: pip install requests")
            return False
