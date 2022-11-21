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

from . import loading, gen_token, content, topic_list, query_id

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
                Horizontal(
                    Static("<", classes="entry-pagination-next"),
                    Input("1", classes="entry-pagination-current"),
                    Static("/999", classes="entry-pagination-last"),
                    Static("⨠", classes="entry-pagination-next"),
                    classes="entry-pagination",
                ),
                classes="entry-horizontal",
            ),
            id="content-body",
        )


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Static("Textual Demo")


logo_part1 = """\
█▀▀ █▄▀ █▀ █
██▄ █░█ ▄█ █"""
logo_part2 = """\
 ▀█▀ █░█ █
 ░█░ █▄█ █"""


class EksiTUIApp(App):
    show_sidebar = reactive(False)
    CSS_PATH = "main.css"
    BINDINGS = [
        ("t", "toggle_dark", "🎨Tema"),
        # ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f", "arama_focus", "Arama"),
        ("h", "about", "Hakkında"),
        # ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        ("ctrl+c,ctrl+q", "app.quit", "🪧Çıkış"),
    ]

    def action_open_link(self, link: str) -> None:
        import webbrowser

        webbrowser.open(link)

    def compose(self) -> ComposeResult:
        self.logo_part1 = Static(logo_part1, classes="logo_part1")
        self.logo_part1.styles.opacity = 0.0
        self.logo_part2 = Static(logo_part2, classes="logo_part2")
        self.logo_part2.styles.opacity = 0.0
        search_input = Input(placeholder="arama", classes="search_input")
        search_input.cursor_blink = False
        yield Horizontal(
            self.logo_part1,
            self.logo_part2,
            search_input,
            classes="top",
        )
        entry = EntryContent()
        yield Vertical(
            Horizontal(TopicList(), entry), Sidebar(classes="-hidden"), Footer()
        )

    def content_format(self, txt: str) -> str:
        # [http: text] -> [link=http:]text[/]
        def repl(m):
            item = re.search(r"(http(.*?)) (.*?)]", m[0]).groups()
            return f"[link={item[0]}]{item[2]}↗[/]"

        txt = re.sub(r"\x5Bhttp.*?]", repl, txt)

        # [ ] -> \[ \]

        # (bkz: baslik) -> (bkz: [link=http:]baslik[/])

        # `:akıllı bkz` -> [link=https://eksisozluk.com/?q={quote(akıllı bkz)}]*[/]
        def repl(m):
            return f"[@click=navigate_page('{query_id.result(token, m[1])}')]*[/]"

        txt = re.sub(r"`:(.*?(?<!\\))`", repl, txt)

        # `hede`
        def repl(m):
            return f"[@click=navigate_page('{query_id.result(token, m[1])}')]{m[1]}[/]"

        txt = re.sub(r"`(.*?(?<!\\))`", repl, txt)

        # linkler
        def repl(m):
            return f"[link={m[0]}]{m[0]}↗[/]"

        txt = re.sub(r"(?<!\x5Blink=)http?\S*", repl, txt)

        return txt

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.navigate_page(event.button.name)

    def smalltext(self, txt: str, type: int = 1) -> str:
        inp = "qwertyuiopasdfghjklzxcvbnmğüşıöç1234567890()-'+=?!$"
        super_chars = "ᑫʷᵉʳᵗʸᵘⁱᵒᵖᵃˢᵈᶠᵍʰʲᵏˡᶻˣᶜᵛᵇⁿᵐᵍᵘᶳᶥᵒᶜ¹²³⁴⁵⁶⁷⁸⁹⁰⁽⁾⁻'⁺⁼ˀꜝᙚ"
        sub_chars = "ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ₁₂₃₄₅₆₇₈₉₀₊₌₍₎₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋"
        return txt.translate(str.maketrans(inp, super_chars if type else sub_chars))

    def navigate_page(self, id) -> None:
        if self.query(".entry-container"):
            self.query(".entry-container").remove()
            self.query(".topic-showall").remove()
        else:
            self.query_one("#loading-container").styles.display = "none"

        cont = content.result(token, id, self.topic_tip)

        # baslik
        self.query_one(".entry-baslik").update(
            f'[@click=navigate_page({cont["Id"]})]{cont["Title"]}[/]'
            + f'[link=https://eksisozluk.com/{cont["Slug"]}--{cont["Id"]}]↗[/]'
        )

        # pagination
        if self.topic_tip == "topic":
            self.query_one(".entry-pagination-current").styles.visibility = "visible"
            self.query_one(".entry-pagination-last").styles.visibility = "visible"
            self.query_one(".entry-pagination-last").update(
                "/" + str(cont["PageCount"])
            )
        else:
            self.query_one(".entry-pagination-current").styles.visibility = "hidden"
            self.query_one(".entry-pagination-last").styles.visibility = "hidden"

        content_body = self.query_one("#content-body")

        # showall more-data
        if self.topic_tip != "entry" and cont["EntryCounts"]["BeforeFirstEntry"]:
            content_body.mount(
                Static(
                    f'↥ [@click=get_showall("popular")]{str(cont["EntryCounts"]["BeforeFirstEntry"])} entry daha[/] ↥',
                    classes="topic-showall",
                )
            )
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

            entry_txt = Static(self.content_format(i["Content"]), classes="entry_txt")
            entry_footer = Static(
                (
                    "[dark_khaki]" + self.smalltext(f"({fav})") + "[/]"
                    if fav != "0"
                    else ""
                )
                + f" [dark_khaki][link=https://eksisozluk.com/biri/{quote(author)}]{author}[/][/dark_khaki]"
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
            print(self.query_one(Input).value)
            id = query_id.result(token, self.query_one(Input).value)
            self.navigate_page(id)

    def on_mount(self):
        self.topic_tip = "topic"
        # animations
        self.logo_part1.styles.animate(
            "opacity", value=1.0, duration=1.1, easing="out_bounce"
        )
        self.logo_part2.styles.animate(
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

    def action_navigate_page(self, id) -> None:
        # !!!! topic_tip
        self.navigate_page(id)

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
