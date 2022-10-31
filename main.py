from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import *
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import Screen
from textual import events

from rich.console import Console
from rich.text import Text
from rich import print

import asyncio
import httpx

from src import gundem, gen_token, content

token = gen_token.result()
topicid = ""


class Content(Vertical):
    pass


class TopicList(Widget):
    def compose(self) -> ComposeResult:
        topbar = Static("[i]gündem " + "bugün")
        topbar.styles.align = ("right", "top")
        yield topbar
        for i in gundem.result(token):  # sorted() "sıralama=alfabe,varsayılan"
            yield Button(
                i[0],
                name=i[1],
            )


class EntryContent(Widget):
    def compose(self) -> ComposeResult:
        if topicid:
            cont = content.result(token, "7250896")
            # yield Static("1/93")
            yield Static(
                # f"""[@click="app.open_link('https://eksisozluk.com/{cont["Slug"]}--{cont["Id"]}')"]{cont["Title"]}[/]""",
                f'[link=https://eksisozluk.com/{cont["Slug"]}--{cont["Id"]}]{cont["Title"]}[/]',
                classes="entry-baslik",
            )
            for i in cont["Entries"]:
                entry_content = Static(i["Content"])
                entry_footer = Static(
                    f'{str(i["FavoriteCount"])} {i["Author"]["Nick"]} {i["Created"]}'
                )
                yield Container(
                    Vertical(entry_content, entry_footer, classes="entry"),
                    classes="entry-container",
                )


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Static("Textual Demo")


logotxt1 = """\
█▀▀ █▄▀ █▀ █
██▄ █░█ ▄█ █"""
logotxt2 = """\
 ▀█▀ █░█ █
 ░█░ █▄█ █"""

righttxt = Static(
    """\
. *  ˚    *    .   ✫       *   * · .      *   ✧  ·       *   * · .       +      ★      ,      ✦             ˚""",
    classes="righttxt",
)


class EksiTUIApp(App):
    show_sidebar = reactive(False)
    CSS_PATH = "main.css"
    BINDINGS = [
        ("t", "toggle_dark", "🎨Tema"),
        ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f", "arama_focus", "Arama"),
        ("h", "about", "Hakkında"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        ("ctrl+c,ctrl+q", "app.quit", "🪧Çıkış"),
    ]

    def action_open_link(self, link: str) -> None:
        import webbrowser

        webbrowser.open(link)

    def compose(self) -> ComposeResult:
        self.loggo = Static(logotxt1, classes="loggo")
        self.loggo.styles.opacity = 0.0
        self.loggo2 = Static(logotxt2, classes="loggo2")
        search_input = Input(placeholder="arama", classes="search_input")
        search_input.cursor_blink = False
        yield Horizontal(
            self.loggo,
            self.loggo2,
            search_input,
            righttxt,
            classes="top",
        )
        # yield Content(QuickIndex())
        entry = EntryContent()
        yield Vertical(
            Horizontal(TopicList(), entry), Sidebar(classes="-hidden"), Footer()
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        topicid = event.button.name
        print(event.button.name)

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+x":
            self.query_one(Input).value = ""
        if event.key == "ctrl+o":
            footer = self.query_one(Footer)
            footer.styles.display = (
                "none" if footer.styles.display == "block" else "block"
            )

    def on_mount(self):
        self.loggo.styles.animate(
            "opacity", value=1.0, duration=1.1, easing="out_bounce"
        )

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_arama_focus(self):
        self.query_one(Input).focus()
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

    def action_about(self) -> None:
        print("hakkinda")

    def action_screenshot(
        self,
        filename: str = "ss.svg",
        path: str = "./img/",
    ) -> None:
        """Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.
        Args:
            filename (str | None, optional): Filename of screenshot, or None to auto-generate. Defaults to None.
            path (str, optional): Path to directory. Defaults to "./".
        """
        self.bell()
        path = self.save_screenshot(filename, path)


if __name__ == "__main__":
    app = EksiTUIApp()
    app.run()
