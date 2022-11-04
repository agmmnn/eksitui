from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import *
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import Screen
from textual import events

from datetime import datetime
import re
from urllib.parse import quote

from . import loading, gen_token, content, topic_list, search

token = gen_token.result()


class TopicList(Widget):
    def compose(self) -> ComposeResult:
        nav = Static(
            "[@click=get_topiclist('popular')]gündem[/] [@click=get_topiclist('today')]bugün[/] [@click=get_topiclist('debe')]debe[/]",
            classes="nav",
        )
        container = Container(id="topic-container")
        list_container = Container(id="topic-container-list")
        for i in topic_list.result(token, "popular"):
            list_container.mount(Button(i[0], name=i[1]))
        container.mount(nav, list_container)
        yield container


class EntryContent(Widget):
    def compose(self) -> ComposeResult:
        yield Container(
            Static(loading.output(), classes="loading"),
            id="loading-container",
        )

        yield Container(
            Horizontal(
                Static(
                    "entry-baslik",
                    classes="entry-baslik",
                ),
                Input("1", classes="entry-pagination"),
                Static("/93"),
                classes="entry-horizontal",
            ),
            id="content-body",
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
            classes="top",
        )
        entry = EntryContent()
        yield Vertical(
            Horizontal(TopicList(), entry), Sidebar(classes="-hidden"), Footer()
        )

    def content_convert(self, txt: str) -> str:
        entry_txt = txt
        # [http: ad] -> [link=http:]ad[/]
        if re.search("^\[http.*\]$", entry_txt):
            pass
        # [ ] -> \[ \]
        # (bkz: baslik) -> (bkz: [link=http:]baslik[/])
        # `:akıllı bkz` -> [link=https://eksisozluk.com/?q={quote(akıllı bkz)}]*[/]
        if re.search("^`:.*`$", entry_txt):
            pass
        # `hede`
        # ayrıca linkler : alt satıra geçince hatalı oluyor

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.query(".entry-container"):
            self.query(".entry-container").remove()
        else:
            self.query_one("#loading-container").styles.display = "none"
        self.navigate_page(event.button.name)

    def smalltext(self, txt: str, type: int = 1) -> str:
        inp = "qwertyuiopasdfghjklzxcvbnmğüşıöç1234567890()-'+=?!$"
        super_chars = "ᑫʷᵉʳᵗʸᵘⁱᵒᵖᵃˢᵈᶠᵍʰʲᵏˡᶻˣᶜᵛᵇⁿᵐᵍᵘᶳᶥᵒᶜ¹²³⁴⁵⁶⁷⁸⁹⁰⁽⁾⁻'⁺⁼ˀꜝᙚ"
        sub_chars = "ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ₁₂₃₄₅₆₇₈₉₀₊₌₍₎₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋"
        return txt.translate(str.maketrans(inp, super_chars if type else sub_chars))

    def navigate_page(self, id) -> None:
        cont = content.result(token, id, self.topic_tip)
        self.query_one(".entry-baslik").update(
            f'[link=https://eksisozluk.com/{cont["Slug"]}--{cont["Id"]}]{cont["Title"]}[/]'
        )
        content_body = self.query_one("#content-body")
        for i in cont["Entries"]:
            try:
                entry_date = datetime.strptime(i["Created"], "%Y-%m-%dT%H:%M:%S.%f")
                entry_date = entry_date.strftime("%d.%m.%Y %H:%M")
            except:
                entry_date = datetime.strptime(i["Created"], "%Y-%m-%dT%H:%M:%S")
                entry_date = entry_date.strftime("%d.%m.%Y")
            entry_id = i["Id"]
            fav = str(i["FavoriteCount"])
            author = i["Author"]["Nick"]

            entry_txt = Static(i["Content"], classes="entry_txt")
            entry_footer = Static(
                ("[green]" + self.smalltext(f"+{fav}") + "[/][i]" if fav != "0" else "")
                + f" [link=https://eksisozluk.com/biri/{author}]{author}[/]"
                + "\n"
                + f"[link=https://eksisozluk.com/entry/{entry_id}]{entry_date}[/]",
                classes="entry-footer",
            )
            ent_cont = Container(
                Vertical(entry_txt, entry_footer, classes="entry"),
                classes="entry-container",
            )
            content_body.mount(ent_cont)

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+x":
            self.query_one(Input).value = ""
        if event.key == "ctrl+o":
            footer = self.query_one(Footer)
            footer.styles.display = (
                "none" if footer.styles.display == "block" else "block"
            )
        if event.key == "enter":
            id = search.result(token, self.query_one(Input).value)
            self.navigate_page(id)

    def on_mount(self):
        self.topic_tip = "topic"
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

    def action_get_topiclist(self, tip: str = "popular") -> None:
        self.topic_tip = "entry" if tip == "debe" else "topic"
        self.query("#topic-container-list").remove()
        list_container = Container(id="topic-container-list")
        for i in topic_list.result(token, tip):
            list_container.mount(Button(i[0], name=i[1]))
        self.query_one("#topic-container").mount(list_container)

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
