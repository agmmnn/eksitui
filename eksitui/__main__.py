from .main import EksiTUIApp
import argparse

__version__ = "0.1"

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


if __name__ == "__main__":
    app = EksiTUIApp()
    app.run()
