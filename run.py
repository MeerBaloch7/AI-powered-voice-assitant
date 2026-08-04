import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Run the speech assistant.")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["voice", "gui", "integrated"],
        default="integrated",
        help="Select application mode: voice, gui, or integrated.",
    )
    parser.add_argument(
        "--trigger",
        choices=["wake", "hotkey", "both"],
        default=None,
        help="Override the config file trigger mode.",
    )
    args = parser.parse_args()

    cmd = [sys.executable, "main.py", "--mode", args.mode]
    if args.trigger:
        cmd += ["--trigger", args.trigger]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
