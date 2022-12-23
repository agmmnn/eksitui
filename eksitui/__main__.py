from .main import EksiTUIApp
import argparse
from importlib_metadata import version

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
ap.add_argument(
    "-v", "--version", action="version", version=f"eksitui {version('eksitui')}"
)
args = ap.parse_args()


def main():
    app = EksiTUIApp()
    word = " ".join(args.word)
    if word:
        print(word)
        app.word = word
    app.run()


if __name__ == "__main__":
    main()
