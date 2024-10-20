import reflex as rx
from rxconfig import config


class State(rx.State):
    """The app state."""
    
    # Track todos: (checked, text, deleted)
    todos: list[list[tuple[bool, str]]] = [[], [], [], []]
    
    # User input from the text box
    user_input: str = ""
    
    # AI output after processing user input
    ai_output: str = ""

    def add_todo_to_box(self):
        if not self.user_input.strip():  # NO WHITESPACE ONLY
            self.user_input = ""  # Set user_input to nothing if invald REAL
            return  # GET OUT
    
        """Add user input to the first empty todo box."""
        for i in range(4):
            if len(self.todos[i]) == min(len(todo) for todo in self.todos):
                # Append a new tuple: (is_checked, user_input, another_flag)
                self.todos[i].append((False, self.user_input))  # Initialize is_checked as False
                break
        self.user_input = ""  # Clear the input field
        
    def toggle_todo_checked(self, box_index: int, todo_index: int):
        """Toggle the checked state of the specified todo item."""
        checked, text = self.todos[box_index][todo_index]
        self.todos[box_index][todo_index] = (not checked, text)  # Toggle checked state
        
    def remove_todo_from_box(self, box_index: int, todo_index: int):
        """Remove the specified todo item."""
        self.todos[box_index].pop(todo_index)


@rx.page(route="/matrix")
def matrixpage() -> rx.Component:
    # Properties of grid cards
    grid_card_props = {
        "height": "40vh",
        "width": "100%",
        "text_align": "center",
        "padding": "20px",
        "overflow_y": "auto"
    }
    
    # Card colors
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
                rx.vstack(
                    rx.foreach(
                        State.todos[i],
                        lambda todo, index=i: rx.hstack(
                            rx.checkbox(
                                checked=todo[0],  # Get the checked status from the tuple
                                on_change=lambda checked, box_index=i, todo_index=index: (
                                    State.toggle_todo_checked(box_index, todo_index)  # Call the toggle method
                                ),
                                variant="surface",
                                color_scheme="gray",
                                size="3"
                            ),
                            rx.button(
                                todo[1],  # Get the task description from the todo tuple
                                style=rx.cond(
                                    todo[0],  # Check if the todo is checked
                                    {"textDecoration": "line-through", "opacity": 0.5},  # Apply strikethrough and make text translucent if checked
                                    {"textDecoration": "none", "opacity": 1}  # No strikethrough and full opacity if not checked
                                ),
                                on_click=lambda box_index=i, todo_index=index: State.remove_todo_from_box(box_index, todo_index),  # Remove the todo on click
                                variant="ghost",  # Make the button transparent
                                color="inherit",  # Inherit color from parent
                                text_align="left",  # Align text to the left
                                size="3",
                                _hover={"textDecoration": "underline"}  # Underline on hover
                            ),
                            spacing="20px"
                        )
                    )
                ),
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
# app = rx.App()
# app.add_page(matrixpage, route="/other")