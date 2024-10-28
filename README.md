# TaskTaka

**TaskTaka** is an intuitive web application designed to help users manage and prioritize their tasks efficiently. By leveraging the **Action-Priority Matrix**, the application categorizes tasks based on Impact and Effort (Low/High). TaskTaka is powered by **Reflex.dev** and incorporates **Gemini**, an AI that interprets user inputs to dynamically assign tasks to the appropriate quadrant of the matrix (Quick Wins, Major Projects, Fill-Ins, or Time Wasters).

## Features

- **AI-Powered Task Management**: The AI helps interpret tasks and sorts them based on the Effort and Impact required.
- **Dynamic Task Updates**: Tasks are automatically updated and moved across the matrix as new data is provided.
- **User-Friendly Interface**: Simple and intuitive design to help users quickly categorize and manage their tasks.

## Installation and Running the Project

To run **TaskTaka** locally, follow these steps:

1. **Clone the repository**:
   ```
   git clone https://github.com/your-repo/tasktaka.git
   cd tasktaka
   ```
2. Set up a Virtual Environment (Optional but Recommended)
To keep the project environment isolated and dependencies portable, you can create a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate  # Activate the virtual environment
```
3. Install Dependencies:
If you don't already have Reflex.dev installed, you can install it using pip:
  ```bash
  pip install reflex.dev
  ```
Initialize project with
  ```bash
  reflex init
  ```
Then, install API library:
```bash
pip install -U google-generativeai
```
4. Run the application:
Once Reflex.dev is installed, you can run the project locally: 
  ```bash
  reflex run
  ```
5. Access the application:
  After running the application, open your browser and navigate to:
  ```http://localhost:3000```

## Use-Case Example
Imagine you are juggling several tasks with varying degrees of importance and complexity. For example:

Imagine you are a project manager with a list of tasks that need to be prioritized. Using TaskTaka, you input each task with details about its expected impact and the effort required. The AI interprets the information and places each task on the Action-Priority Matrix. High-impact, low-effort tasks appear in the top-right quadrant, indicating they should be prioritized. As you complete tasks or as new tasks come in, the matrix updates in real time, helping you stay focused and organized.

Task 1: "Complete client proposal" (High Impact, High Effort) → Major Projects
Task 2: "Reply to emails" (Low Impact, Low Effort) → Fill-Ins
Task 3: "Plan team lunch" (Low Impact, High Effort) → Time Wasters
Task 4: "Prepare for strategy meeting" (High Impact, Low Effort) → Quick Wins
You can simply enter these tasks into TaskTaka, and the AI will intelligently place them in the appropriate quadrant based on the impact and effort levels.

## Special Considerations
Customization: You can tweak the AI's interpretation model to fit your specific task management needs.
Dependencies: Ensure that you have Python and Reflex.dev installed. Additional packages required for AI handling may need to be installed based on the Reflex.dev setup.
Scaling: TaskTaka is designed to handle small to medium-sized task lists. Performance may degrade if handling a large number of tasks simultaneously.

## Project Directory
```
.
├── README.md
├── TaskTaka
│   ├── TaskTaka.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── TaskTaka.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   └── matrix.cpython-312.pyc
│   └── matrix.py
├── __pycache__
│   └── rxconfig.cpython-312.pyc
├── assets
│   └── favicon.ico
├── requirements.txt
└── rxconfig.py
```

# Contributors
Freddie Gutierrez, Leo Zhang, Gevilee Mariane Verango, Wallace Tang

(CAL HACKS 11.0 CCSF CS Club)

License
