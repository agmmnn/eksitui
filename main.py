from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import *
from textual.widget import Widget
from rich.console import Console
from rich.text import Text
from rich import print
from textual.reactive import reactive

gundem = [
    "yazarların favori bilgisayar komutları",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
    "26 ekim 2022 ümit özdağ'ın sedat pekerle görüşmesi",
]


class Content(Vertical):
    pass


class TopicList(Widget):
    def compose(self) -> ComposeResult:
        for i in sorted(gundem, reverse=True):
            yield Button(i, variant="default")


class QuickIndex(Widget):
    # yield Static("💫 gündem:")
    def compose(self) -> ComposeResult:
        for i in sorted(gundem, reverse=True):
            yield Button(i, variant="default")


content = """
projelere çalışırken el alışkanlığı oldu hatta google da surfing takılırken istemsizce ctrl+s komutu giriyorum.alışkanlığı oldu hatta google da surfing takılırken istemsizce ctrl+s koalışkanlığı oldu hatta google da surfing takılırken istemsizce...
(bkz: [@click="app.open_link('https://eksisozluk.com/?q=lol')"]lol[/])

(17) · 26.10.2022 15:18 · [@click="app.open_link('https://eksisozluk.com/biri/yazar')"]@yazar[/]
[on green] ⋮ [/] 🔗entry linkini koyala | 📷ekran görüntüsü(.svg)

"""


class EntryContent(Widget):
    def compose(self) -> ComposeResult:
        # yield Static(
        #     """[green][@click="app.open_link('https://eksisozluk.com/memur-kalitesinin-artmasi-icin-cozum-onerileri--5912619')"][b]yazarların favori bilgisayar komutları[/b][/][/green]"""
        # )
        yield Static(
            """[bold green link=https://eksisozluk.com/memur-kalitesinin-artmasi-icin-cozum-onerileri--5912619]yazarların favori bilgisayar komutları[/]"""
        )
        yield Static("1/93")
        yield Static(content * 3)


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Static("Textual Demo")


logotxt = """\
█▀▀ █▄▀ █▀ █ ▀█▀ █░█ █
██▄ █░█ ▄█ █ ░█░ █▄█ █"""


class EksiTUIApp(App):
    show_sidebar = reactive(False)
    CSS_PATH = "main.css"
    BINDINGS = [
        ("t", "toggle_dark", "🎨Tema"),
        ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f", "app.arama_focus", "Arama"),
        ("h", "toggle_sidebar2", "Hakkında"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        ("ctrl+c,ctrl+q", "app.quit", "🪧 Çıkış"),
    ]

    def action_open_link(self, link: str) -> None:
        import webbrowser

        webbrowser.open(link)

    def compose(self) -> ComposeResult:
        loggo = Static(logotxt, classes="loggo")
        search_input = Input(placeholder="ara 🔎", classes="search_input")
        search_input.cursor_blink = False
        yield Horizontal(loggo, search_input, classes="top")
        # yield Content(QuickIndex())
        entry = EntryContent()
        yield Vertical(
            Horizontal(TopicList(), entry), Sidebar(classes="-hidden"), Footer()
        )

    # def on_button_pressed(self) -> None:
    #     self.exit()

    def action_toggle_dark(self):
        self.dark = not self.dark

    def arama_focus(self):
        print("focus input")

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")


if __name__ == "__main__":
    app = EksiTUIApp()
    app.run()
