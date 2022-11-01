from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import *
from textual.widget import Widget
from textual.reactive import reactive
from textual.screen import Screen
from textual import events


class AramaDropdown(Widget):
    def compose(self) -> ComposeResult:
        yield Button("Primary!", variant="primary")

    def on_mount(self) -> None:
        print(
            "AramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdown"
        )

    def focus(self):
        print(
            "AramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdownAramaDropdown"
        )


class MyApp(App):
    BINDINGS = [
        ("f", "set_f", "Red"),
    ]

    def compose(self) -> ComposeResult:
        yield AramaDropdown()
        yield Static("eeee")
        yield Container(id="cont")

    def on_mount(self) -> None:
        # self.mount(Static("hello"), header=Header())
        self.topic_tip = "sdf"

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+x":
            self.query_one("#cont").render()
            sta = Static("hello")
            self.query_one("#cont").mount(sta)
            self.query_one("#cont").refresh(layout=True)
        if event.key == "ctrl+t":
            self.query_one("#cont").remove()
            print(self.topic_tip)
