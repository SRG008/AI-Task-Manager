# AI-Task-Manager
An AI integrated task completion and task handler tool a demo project for learning Agentic AI 
1. Open PowerShell in your new project folder
cd E:\AI-Task-Manager


2. Create a virtual environment
If you haven't already created one:
python -m venv .venv


3. Activate it
.\.venv\Scripts\Activate.ps1


If PowerShell blocks activation:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1


4. Install the required packages
Run:
python -m pip install --upgrade pip
python -m pip install google-genai python-dotenv


5. Run your application
python main.py