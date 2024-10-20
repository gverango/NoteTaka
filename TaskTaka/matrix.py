import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    
    # seeing if input in each grid is possible
    todos: list[list[str]] = [[], [], [], []]
    
    # Store the user input from the text box
    user_input: str = ""
    
    # Store what the AI outputs after processing the user input
    ai_output: str = ""
    
    # Function to handle adding the user input to the first empty box
    def add_todo_to_box(self):
        for i in range(4):
            if len(self.todos[i]) == min(len(todo) for todo in self.todos):
                self.todos[i].append(self.user_input)
                break
        self.user_input = ""  #clears the input field


@rx.page(route="/other")
def matrixpage() -> rx.Component:
    # properties of grid cards
    grid_card_props = {
        "height": "40vh",
        "width": "100%",
        "text_align": "center",
        "padding": "20px",
        "overflow_y": "auto"
    }
    
    card_colors = [
        {"background_color": "#FFC90E", "color": "black"},
        {"background_color": "#E00A0D", "color": "white"},
        {"background_color": "#1E90FF", "color": "white"},
        {"background_color": "#B5E61D", "color": "black"},
    ]
    
    # Create the grid layout for the task matrix
    grid = rx.grid(
        *[
            rx.card(
                rx.vstack(rx.foreach(State.todos[i], lambda item: rx.text(item))),
                background_color=card_colors[i]["background_color"],
                color=card_colors[i]["color"],
                **grid_card_props  # Apply common card properties
            )
            for i in range(4)
        ],
        columns="2",   # Keep 2 columns for the grid layout
        gap="20px",    # Add gap between the cards for breathing room
        width="800px", # Fixed width for the grid to avoid zoom issues
        margin="auto", # Center the grid
    )
    
    return rx.container(
        rx.vstack(  # Stack heading, grid, and input vertically
            # Heading
            rx.heading(
                "Effort-Impact Task Matrix", 
                font_size="40px", 
                text_align="center", 
                margin_bottom="30px"
            ),
            
            # Grid displaying the four boxes
            grid,
            
            # Input area for adding a new to-do
            rx.hstack(
                # Text input box
                rx.input(
                    placeholder="Describe a task", 
                    value=State.user_input,
                    on_change=State.set_user_input, 
                    width="400px",  # Set input width
                ),
                # Button to submit the task
                rx.button(
                    "Add Task",
                    on_click=State.add_todo_to_box,
                    background_color="#1E90FF",
                    color="white",
                    padding="10px",
                    _hover={"cursor": "pointer"}
                ),
                justify_content="center",  # Center the input and button
            ),
            
            align_items="center",  # Center everything
            width="100%",  # Ensure the container stays centered
        ),
        padding="20px",
        max_width="900px",  # Control the overall width of the container
        margin="auto",  # Center the container horizontally
    )


# Initialize the app and add the page
#app = rx.App()
#app.add_page(matrixpage, route="/other")