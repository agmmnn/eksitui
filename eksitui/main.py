from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import *
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import Screen
from textual import events, log

from datetime import datetime
import re
from urllib.parse import quote

from . import loading, gen_token, content, topic_list, query_id, utils

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
            list_container.mount(Button(i[0], name=str(i[1]) + ":popular"))
        container.mount(nav, list_container)
        yield container


class EntryContent(Widget):
    def compose(self) -> ComposeResult:
        pagination = Horizontal(
            Static(
                "[@click=pager('previous')]<[/]", classes="entry-pagination-previous"
            ),
            Input("1", classes="entry-pagination-current", name="pager_go"),
            Static("/[@click=pager_go(999)]999[/]", classes="entry-pagination-last"),
            Static("[@click=pager('next')]>[/]", classes="entry-pagination-next"),
            classes="entry-pagination",
        )

        yield Container(
            Static(loading.output(), classes="loading"),
            id="loading-container",
        )

        yield Container(
            Static(
                "entry-baslik",
                classes="entry-baslik",
            ),
            pagination,
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
    baslik = reactive("baslik")
    id = reactive(0)
    currentpage = reactive(1)
    lastpage = 0
    show_sidebar = reactive(False)

    word = ""

    CSS_PATH = "main.css"
    BINDINGS = [
        ("t", "toggle_dark", "🎨Tema"),
        # ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f", "arama_focus", "Arama"),
        # ("l", "live_mode", "💫Live Mode"),
        # ("h", "about", "Hakkında"),
        # ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        ("q", "pager('previous')", "←Önceki"),
        ("w", "pager('next')", "→Sonraki"),
        ("ctrl+c,ctrl+q", "app.quit", "🪧Çıkış"),
    ]

    def compose(self) -> ComposeResult:
        self.logo_part1 = Static(logo_part1, classes="logo_part1")
        self.logo_part2 = Static(logo_part2, classes="logo_part2")
        search_input = Input(placeholder="arama", classes="search-input", name="search")
        search_input.cursor_blink = False
        yield Horizontal(
            self.logo_part1,
            self.logo_part2,
            search_input,
            classes="top",
        )

        yield Vertical(
            Horizontal(TopicList(), EntryContent()),
            Sidebar(classes="-hidden"),
            classes="root",
        )
        yield Footer()

    def content_format(self, txt: str) -> str:
        # ' -> ‛
        txt = txt.replace("'", "‛")

        # [ -> \[
        txt = re.sub(r"(?!.*\[http)\[", "\[", txt)

        # [http: text] -> [link=http:]text[/]
        # bug: 7475207?p=6
        def repl(m):
            item = re.search(r"(http(.*?)) (.*?)]", m[0]).groups()
            return f"[link={item[0]}]{item[2]}↗[/]"

        try:
            txt = re.sub(r"\x5Bhttp.*?]", repl, txt)
        except:
            pass

        # (bkz: baslik) -> (bkz: [link=http:]baslik[/])
        def repl(m):
            return f"(bkz: [@click=navigate_page_with_query('{m[1]}')]{m[1]}[/])"

        txt = re.sub(r"\(bkz: (.*?(?<!\\))\)", repl, txt)

        # `:akıllı bkz` -> [link=https://eksisozluk.com/?q={quote(akıllı bkz)}]*[/]
        # bug: 7475207
        # def repl(m):
        #     return f"[@click=navigate_page_with_query('{m[1]}')]*[/]"

        # txt = re.sub(r"`:(.*?(?<!\\))`", repl, txt)

        # `hede`
        # bug: gizemi çözüldüğünde rahatlatacak şeyler p=100
        def repl(m):
            return f"[@click=navigate_page_with_query('{m[1]}')]{m[1]}[/]"

        txt = re.sub(r"`(.*?(?<!\\))`", repl, txt)

        # linkler
        # bug: ara p=11
        def repl(m):
            return f"[link={m[0]}]{m[0]}↗[/]"

        txt = re.sub(r"(?<!\x5Blink=)(http|https):\/\/?\S*", repl, txt)

        # with open("test.txt", "w", encoding="utf-8") as f:
        #     f.write(txt)
        return txt

    def watch_baslik(self, value):
        self.query_one(".entry-baslik").update(value)

    def navigate_page(self, id, topic_tip: str, categ: str = "", page: int = 1) -> None:
        if self.query(".entry-container"):
            self.query(".entry-container").remove()
            self.query(".topic-showall").remove()
        else:
            self.query_one("#loading-container").styles.display = "none"

        cont = content.result(token, topic_tip, id, categ, page)
        self.id = cont["Id"]
        self.currentpage = page
        # baslik
        self.baslik = (
            f'[@click=navigate_page({cont["Id"]})]{cont["Title"]}[/]'
            + f'[link=https://eksisozluk.com/{cont["Slug"]}--{cont["Id"]}]↗[/]'
        )

        # pagination
        if self.topic_tip != "entry":
            self.lastpage = cont["PageCount"]
            self.query_one(".entry-pagination-previous").styles.visibility = "visible"
            self.query_one(".entry-pagination-current").styles.visibility = "visible"
            self.query_one(".entry-pagination-last").styles.visibility = "visible"
            self.query_one(".entry-pagination-next").styles.visibility = "visible"
            self.query_one(".entry-pagination-last").update(
                f"/[@click=pager_go({cont['PageCount']})]{cont['PageCount']}[/]"
            )
        else:
            self.query_one(".entry-pagination-previous").styles.visibility = "hidden"
            self.query_one(".entry-pagination-current").styles.visibility = "hidden"
            self.query_one(".entry-pagination-last").styles.visibility = "hidden"
            self.query_one(".entry-pagination-next").styles.visibility = "hidden"

        content_body = self.query_one("#content-body")

        # showall more-data
        if (
            self.topic_tip != "entry"
            and self.categ != ""
            and cont["EntryCounts"]["BeforeFirstEntry"]
        ):
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

            entry_txt = Static(self.content_format(i["Content"]), classes="entry-txt")
            entry_footer = Static(
                (
                    "[dark_khaki]" + utils.smalltext(f"({fav})") + "[/]"
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
        self.query_one(".entry-baslik").scroll_visible()
        # content_body.mount(Static(f'↥[@click=get_showall("popular")]Başa çık.[/]'))

    def on_mount(self):
        self.topic_tip = "topic"
        self.categ = "popular"
        # animations
        self.logo_part1.styles.animate(
            "opacity", value=1.0, duration=1.8, easing="out_bounce"
        )
        self.logo_part2.styles.animate(
            "opacity", value=1.0, duration=1.8, easing="out_bounce"
        )
        if self.word != "":
            self.action_navigate_page_with_query(self.word)

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+x":
            self.query_one(".search-input").value = ""
        if event.key == "ctrl+o":
            footer = self.query_one(Footer)
            footer.styles.display = (
                "none" if footer.styles.display == "block" else "block"
            )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.set_focus(None)
        if event.input.name == "search":
            self.action_navigate_page_with_query(event.value)
        elif event.input.name == "pager_go" and event.value.isnumeric():
            if int(event.value) <= self.lastpage and int(event.value) >= 1:
                self.action_pager_go(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        i = event.button.name.split(":")
        self.categ = i[1]
        self.navigate_page(i[0], self.topic_tip, i[1])

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_arama_focus(self):
        self.query_one(".search-input").focus()

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
        print("about")

    def action_navigate_page(self, id) -> None:
        self.categ = ""
        self.navigate_page(id, "topic", "")

    def action_navigate_page_with_query(self, term) -> None:
        self.categ = ""
        id = query_id.result(token, quote(term))
        if id:
            self.navigate_page(id, "topic", "")

    def watch_currentpage(self, value):
        self.query_one(".entry-pagination-current").value = str(self.currentpage)

    def action_pager(self, act) -> None:
        if self.id:
            if act == "next":
                if self.currentpage != self.lastpage:
                    self.navigate_page(
                        self.id, "topic", self.categ, self.currentpage + 1
                    )
                else:
                    self.navigate_page(self.id, "topic", self.categ, 1)
            elif act == "previous":
                if self.currentpage != 1:
                    self.navigate_page(
                        self.id, "topic", self.categ, self.currentpage - 1
                    )
                else:
                    self.navigate_page(self.id, "topic", self.categ, self.lastpage)

    def action_pager_go(self, p: int) -> None:
        self.navigate_page(self.id, "topic", self.categ, p)

    def action_get_topiclist(self, tip: str = "popular") -> None:
        self.topic_tip = "entry" if tip == "debe" else "topic"
        self.categ = tip if tip != "debe" else ""

        self.query("#topic-container-list").remove()
        list_container = Container(id="topic-container-list")
        for i in topic_list.result(token, tip):
            list_container.mount(Button(i[0], name=str(i[1]) + ":" + self.categ))
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
