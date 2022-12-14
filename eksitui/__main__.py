from .main import EksiTUIApp
import argparse

__version__ = "0.1.2"

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
ap.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
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
