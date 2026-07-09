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
    args = parser.parse_args()

    subprocess.run([sys.executable, "main.py", "--mode", args.mode], check=True)


if __name__ == "__main__":
    main()
