import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...
  
@rx.page(route="/other")  
def matrixpage() -> rx.Component:
    return rx.container()

#app = rx.App()
#app.add_page(matrixpage, route="/other")