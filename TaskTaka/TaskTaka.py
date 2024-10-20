"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .matrix import matrixpage


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to TaskTaka!", size="9", text_align="center"),
            rx.text(
                "One Stop Task Management at Your Fingertips",
                #rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="7",
                text_align="center",
            ),
            rx.link(
                rx.button("Try it out!", _hover={"cursor": "pointer"}),
                #href="matrix.py",
                is_external=False,
                on_click=rx.redirect("/other"),
                text_align="center",
            ),
            spacing="5",
            justify="center",
            align_items="center",
            min_height="85vh",
        )
        #rx.logo()
    )


app = rx.App()
app.add_page(index)