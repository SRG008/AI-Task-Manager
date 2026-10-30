
# AI Task Manager 🤖

An AI-powered task management application built with **Python, Google Gemini API, and SQLite**.

This is a demo project created to learn and understand **Agentic AI**, including how AI agents interpret user requests, select tools, execute functions, and interact with a database.

## 🚀 Features

- Add new tasks using natural language.
- View all saved tasks.
- Mark tasks as completed.
- Store tasks locally using SQLite.
- Integrate Google Gemini as the AI model.
- Use AI function calling to select and execute Python tools.

## 🛠️ Tech Stack

- **Language:** Python
- **AI Model:** Google Gemini
- **AI SDK:** Google GenAI (`google-genai`)
- **Database:** SQLite
- **Environment Variables:** python-dotenv

## 📁 Project Structure

```text
AI-Task-Manager/
│
├── main.py              # Main AI agent
├── tools.py             # Agent tool definitions
├── database.py          # SQLite database operations
├── requirements.txt     # Python dependencies
├── .env                 # Gemini API key (not committed)
├── .gitignore           # Git ignored files
└── README.md            # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```powershell
git clone <your-repository-url>
cd AI-Task-Manager
```

Alternatively, open PowerShell in your existing project directory:

```powershell
cd E:\AI-Task-Manager
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
```

The execution policy change applies only to the current PowerShell session.

**Windows Command Prompt (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

After activation, your terminal should display `(.venv)`.

### 4. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` is not available, install the packages manually:

```powershell
python -m pip install google-genai python-dotenv
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can generate an API key using [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never commit your `.env` file or API key to GitHub.

### 6. Run the Application

```powershell
python main.py
```

## 💬 Example Usage

**Start the application:**

```text
PERSONAL TASK ASSISTANT

Available operations:
- Add tasks
- List tasks
- Complete tasks

Type 'exit' or 'quit' to stop.
```

**Add a task:**

```text
You: Add a task Learn Python from scratch

[Agent] Executing tool: add_task_tool

Assistant: Task added successfully.
```

**List tasks:**

```text
You: Show me all my tasks

[Agent] Executing tool: list_tasks_tool

Assistant:
ID: 1 | Learn Python from scratch | Pending
```

**Complete a task:**

```text
You: Mark task 1 as completed

[Agent] Executing tool: complete_task_tool

Assistant: Task 1 marked as completed.
```

## 🧠 How the AI Agent Works

The application follows a tool-calling workflow:

```text
          User Request
               |
               v
         Gemini AI Model
               |
               v
      Understands the Request
               |
               v
       Selects a Python Tool
               |
               v
         Executes the Tool
               |
               v
         SQLite Database
               |
               v
        Returns Tool Result
               |
               v
         Gemini AI Model
               |
               v
         Final Response
```

### Available Agent Tools

| Tool | Description |
|------|-------------|
| `add_task_tool()` | Adds a new task |
| `list_tasks_tool()` | Retrieves saved tasks |
| `complete_task_tool()` | Marks a task as completed |

The AI model decides which tool to use based on the user's natural-language request.

The actual database operations are executed by Python functions.

## 🔐 Security

Ensure your `.gitignore` includes:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
tasks.db
```

This prevents API keys, virtual environments, and local database files from being committed.

## 📚 Learning Objectives

This project demonstrates:

1. Fundamentals of Agentic AI.
2. Integrating an LLM into a Python application.
3. AI tool selection and function calling.
4. Executing Python functions through AI-generated tool requests.
5. SQLite database integration.
6. Building a basic single-agent application.

## 🔮 Future Enhancements

- Add task deletion and editing.
- Support task priorities and deadlines.
- Introduce conversation memory.
- Add multiple AI agents.
- Build a web interface.
- Explore LangChain and LangGraph.
- Add automated task scheduling.

## 📝 Project Status

**Learning / Demo Project**

This project is intended for educational purposes and experimentation with Agentic AI concepts.

## 📄 License

No license has been specified yet.
