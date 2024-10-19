import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...
    
def otherpage()->rx.Component:
    return rx.box("new page")

app = rx.App()
app.add_page(otherpage, route="/other")