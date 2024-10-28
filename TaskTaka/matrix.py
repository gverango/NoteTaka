import reflex as rx
import os
import google.generativeai as genai
from google.generativeai import configure



# Loads environment variables from Github Repository Secrets, initializes GEMINI_API_KEY with secret one 
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
if not GEMINI_API_KEY: #error if backend retrieval unsuccessful
    raise ValueError("API Key not found. Make sure GEMINI_API_KEY is set in the backend.env file")

# Set the API key for the Gemini client, from Google Gemini API Quickstart guide
genai.configure(api_key=GEMINI_API_KEY)


class State(rx.State):
    """The app state."""

# Pink going hard on the tuple based todo tracker


    # Track todos: (checked, text)
    todos: list[list[tuple[bool, str]]] = [[], [], [], []]
    
    # User input from the text box
    user_input: str = ""
    
    # AI output after processing user input, to be used in API call
    ai_output: str = ""

    async def add_todo_to_box(self):
        if not self.user_input.strip():
            self.user_input = ""  # Clear the input if empty
            return

        # Call the Gemini AI API to categorize the task
        category, explanation = await self.call_gemini_api(self.user_input)

        # map category to one of the quadrants using a dictionary(0 = Low Effort, Low Impact)
        quadrant_mapping = {
            "low_effort_high_impact": 0, # quick wins, yellow
            "high_effort_high_impact": 1, # major projects, red
            "low_effort_low_impact": 2, # fill ins, blue
            "high_effort_low_impact": 3, #time wasters, green
        }

        # Get the corresponding quadrant for the task
        quadrant = quadrant_mapping.get(category, 2)  # Default to "Fill-Ins" if no match

        # Append the task (is_checked, text) to the appropriate quadrant
        self.todos[quadrant].append((False, self.user_input))  # Initialize as unchecked

        # Clear the input field and store the AI explanation
        self.user_input = ""
        self.ai_output = explanation




# Freddie's collab on the eisen-hower matrix
    async def call_gemini_api(self, task_description: str):
        try:
            # Create an instance of the GenerativeModel
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Gemini AI prompt that appears at the bottom of the screen
            response = model.generate_content(
                f"Please categorize the following task into one of the categories: "
                f"low effort high impact, high effort high impact, low effort low impact, "
                f"or high effort low impact. Task description: '{task_description}'"
        )

# Gev's solution for AI task sorting
            # Extract the AI response text
            result_text = response.text.lower()

            # Searches dictionary and sets todo category
            if "low effort" in result_text and "high impact" in result_text:
                category = "low_effort_high_impact"
            elif "high effort" in result_text and "high impact" in result_text:
                category = "high_effort_high_impact"
            elif "low effort" in result_text and "low impact" in result_text:
                category = "low_effort_low_impact"
            elif "high effort" in result_text and "low impact" in result_text:
                category = "high_effort_low_impact"
            else:
            # Default category if interpretation fails
                category = "low_effort_low_impact" #fill ins

            return category, result_text  # uses AI's explanation as result text

        except Exception as e: #appears when the generate content prompt is faulty
            return "low_effort_low_impact", f"Error calling Gemini AI: {str(e)}"


    def toggle_todo_checked(self, box_index: int, todo_index: int):
        """Toggle the checked state of the specified todo item."""
        checked, text = self.todos[box_index][todo_index]
        self.todos[box_index][todo_index] = (not checked, text)  # Toggle checked state
        
    def remove_todo_from_box(self, box_index: int, todo_index: int):
        """Remove the specified todo item."""
        self.todos[box_index].pop(todo_index)


@rx.page(route="/matrix")
def matrixpage() -> rx.Component:
    #reflex uses color_mode_cond to switch item color based on the theme
    axis_color = rx.color_mode_cond(
        light="black",  # axis color in light
        dark="white"    # axis color in dark
    )

    # Properties of the cards (as before)
    grid_card_props = {
        "flex": "1",  # Make each card flexible to fill available space
        "height": "100%",  # card and header should fill respect quadrant
        "width": "100%",   # Equal widths across quadrants
        "text_align": "center",
        "padding": "20px",
        "overflow_y": "auto"
    }

    grid_button_props = {
        "max_width": "350px",
        "overflow": "visible",
        "white_space": "normal",
        "word_wrap": "break-words",
        "word_break": "break-all",  # word wrap for long words
        "color": "inherit",
        "text_align": "left",
        "variant": "ghost",  # button transparent
        "size": "3",
        "_hover": {"textDecoration": "underline"}  # Underline on hover
    }

    card_subtitles = [
        "Quick Wins",
        "Major Projects",
        "Fill-Ins",
        "Time Wasters"
    ]

    # CARD COLORS
    card_colors = [
        {"background_color": "#FFC90E", "color": "black"},  # yellow, low effort, high impact 
        {"background_color": "#E00A0D", "color": "white"},  # red, high effort, high impact
        {"background_color": "#1E90FF", "color": "white"},  # blue low effort, low impact
        {"background_color": "#B5E61D", "color": "black"},  # green, high effort, low impact
    ]

    # Modify the quadrant_layout lambda to include on_click event for task removal
    quadrant_layout = lambda subtitle, todos, box_index, color: rx.vstack(
        rx.text(subtitle, font_size="24px", font_weight="bold", text_align="center", margin_bottom="5px"),
        rx.card(
            rx.vstack(
                rx.foreach(
                    todos,
                    lambda todo, todo_index: rx.hstack(
                        rx.checkbox(
                            checked=todo[0],  # Checked state of the task
                            on_change=lambda checked, box=box_index, todo_idx=todo_index: (
                                State.toggle_todo_checked(box, todo_idx)  # Toggling checked state
                            ),
                            variant="surface",
                            color_scheme="gray",
                            size="3"
                        ),
                        rx.button(
                            todo[1],  # Task text
                            style=rx.cond(
                                todo[0],  # If the task is checked, apply strikethrough
                                {"textDecoration": "line-through", "opacity": 0.5},
                                {"textDecoration": "none", "opacity": 1}
                            ),
                            on_click=lambda box=box_index, todo_idx=todo_index: State.remove_todo_from_box(box, todo_idx),
                            **grid_button_props
                        ),
                        spacing="15px"
                    )
                )
            ),
            background_color=color["background_color"],
            color=color["color"],
            **grid_card_props
        ),
        width="100%",  # Ensuring the quadrant fills available width
        height="100%", # Ensuring the quadrant fills available height
        padding="10px"
    )
    # Define the grid layout for the four quadrants
    grid_layout = rx.grid(
        # Top-left quadrant (Quick Wins)
        quadrant_layout(card_subtitles[0], State.todos[0], 0, card_colors[0]),
        # Top-right quadrant (Major Projects)
        quadrant_layout(card_subtitles[1], State.todos[1], 1, card_colors[1]),
        # Bottom-left quadrant (Fill-Ins)
        quadrant_layout(card_subtitles[2], State.todos[2], 2, card_colors[2]),
        # Bottom-right quadrant (Time Wasters)
        quadrant_layout(card_subtitles[3], State.todos[3], 3, card_colors[3]),
        columns="1fr 1fr",  # Two columns
        rows="1fr 1fr",  # Two rows
        gap="20px",
        width="800px",  # Fixed width for the grid
        height="600px",  # Fixed height for the grid
        margin="auto",  # Center the grid
        position="relative"  # Relative for the axis overlay
    )

    # Horizontal and Vertical lines
    horizontal_line = rx.box(
        position="absolute",
        top="50%",  # Center the horizontal line
        left="0",  # Start from the left edge
        right="0",  # Stretch to the right edge
        height="2px",
        background_color=axis_color,
        z_index="10"  # Ensure it appears on top of content
    )

    vertical_line = rx.box(
        position="absolute",
        top="0",  # Start from the top edge
        bottom="0",  # Stretch to the bottom edge
        left="50%",  # Center the vertical line
        width="2px",
        background_color=axis_color,
        z_index="10"  # Ensure it appears on top of content
    )

    # Return the layout with axis lines and the input section
    return rx.container(
        rx.vstack(
            rx.box(
                grid_layout,  # The grid layout for the quadrants
                horizontal_line,  # Adding the horizontal axis
                vertical_line,  # Adding the vertical axis
                position="relative",
                width="100%",
                height="600px",  # Fixed height for the container
            ),
            # Input area for adding a new to-do at the bottom
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="Describe a task",
                        value=State.user_input,
                        on_change=State.set_user_input,
                        width="400px",
                    ),
                    rx.button(
                        "Add Task",
                        on_click=State.add_todo_to_box,
                        background_color="#1E90FF",
                        color="white",
                        padding="10px",
                        _hover={"cursor": "pointer"}
                    ),
                    justify_content="center",
                ),
                position="relative",
                width="100%",
                padding="10px",
                margin_top="20px"
            ),
            # Displays AI explanation at the bottom of the page
            rx.text(f"AI says: {State.ai_output}", margin_top="20px", color="gray"),
            align_items="center",
            width="100%",
            position="relative",
        ),
        padding="20px",
        max_width="900px",
        margin="auto",
    )


# Initialize the app and add the page
# app = rx.App()
# app.add_page(matrixpage, route="/other")