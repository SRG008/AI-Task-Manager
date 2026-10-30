
import inspect
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from database import initialize_database
from tools import TOOL_FUNCTIONS


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

load_dotenv(PROJECT_DIR / ".env")

MODEL = "gemini-3.6-flash"

MAX_ITERATIONS = 5

REQUEST_TIMEOUT = 100000


# --------------------------------------------------
# 2. Initialize Gemini client
# --------------------------------------------------

def create_gemini_client():
    """Create Gemini client using API key."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please check your .env file."
        )

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=REQUEST_TIMEOUT
        )
    )


client = create_gemini_client()


# --------------------------------------------------
# 3. Convert Python functions into Gemini tools
# --------------------------------------------------

def convert_tools_for_gemini(tool_functions):

    declarations = []

    for name, function in tool_functions.items():

        signature = inspect.signature(function)

        properties = {}
        required = []

        for param_name, param in signature.parameters.items():

            annotation = param.annotation

            if annotation is int:
                param_type = "INTEGER"

            elif annotation is float:
                param_type = "NUMBER"

            elif annotation is bool:
                param_type = "BOOLEAN"

            else:
                param_type = "STRING"

            properties[param_name] = types.Schema(
                type=param_type,
                description=f"The {param_name} argument."
            )

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        declaration = types.FunctionDeclaration(
            name=name,
            description=(
                inspect.getdoc(function)
                or f"Execute the {name} operation."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties=properties,
                required=required
            )
        )

        declarations.append(declaration)

    return declarations


GEMINI_TOOLS = [
    types.Tool(
        function_declarations=convert_tools_for_gemini(
            TOOL_FUNCTIONS
        )
    )
]


# --------------------------------------------------
# 4. Execute Python tools
# --------------------------------------------------

def execute_tool(function_call):
    """Execute the Python function requested by Gemini."""

    name = function_call.name

    arguments = dict(function_call.args or {})

    print(f"\n[Tool] Requested: {name}")
    print(f"[Tool] Arguments: {arguments}")

    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        return {
            "success": False,
            "error": f"Unknown tool: {name}"
        }

    try:

        result = function(**arguments)

        print(f"[Tool] Result: {result}")

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:

        print(f"[Tool Error] {exc}")

        return {
            "success": False,
            "error": str(exc)
        }


# --------------------------------------------------
# 5. Call Gemini
# --------------------------------------------------

def call_gemini(contents):

    print("\n[Agent] Sending request to Gemini...")

    start_time = time.time()

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=GEMINI_TOOLS,
            temperature=0.2
        )
    )

    elapsed = time.time() - start_time

    print(
        f"[Agent] Gemini responded in "
        f"{elapsed:.2f} seconds."
    )

    return response


# --------------------------------------------------
# 6. Run the agent
# --------------------------------------------------

def run_agent(user_message):
    """Run the agent and execute tools when requested."""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_message)
            ]
        )
    ]

    for iteration in range(MAX_ITERATIONS):

        print(
            f"\n[Agent] Iteration "
            f"{iteration + 1}/{MAX_ITERATIONS}"
        )

        # Ask Gemini what to do.
        response = call_gemini(contents)

        if not response.candidates:
            return "Gemini returned no response."

        model_content = response.candidates[0].content

        # Preserve Gemini's response in conversation history.
        contents.append(model_content)

        # Check whether Gemini wants to execute a tool.
        function_calls = response.function_calls or []

        # If no tool is requested, return Gemini's answer.
        if not function_calls:

            answer = response.text or "No response from Gemini."

            print(f"\nAssistant: {answer}")

            return answer

        # Execute requested tools.
        function_response_parts = []

        for function_call in function_calls:

            result = execute_tool(function_call)

            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response=result
                )
            )

        # Send the tool results back to Gemini.
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts
            )
        )

    return (
        "Maximum agent iterations reached. "
        "Please try a simpler request."
    )


# --------------------------------------------------
# 7. Application entry point
# --------------------------------------------------

def main():

    initialize_database()

    print("=" * 45)
    print("PERSONAL TASK ASSISTANT")
    print("=" * 45)

    print(f"Model: {MODEL}")

    print("\nAvailable operations:")
    print("- Add tasks")
    print("- List tasks")
    print("- Complete tasks")

    print("\nType 'exit' or 'quit' to stop.")

    while True:

        try:

            user_message = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")
            break

        if user_message.lower() in {"exit", "quit"}:

            print("Goodbye!")
            break

        if not user_message:
            continue

        try:

            run_agent(user_message)

        except Exception as exc:

            print(
                f"\n[Error] {type(exc).__name__}: {exc}"
            )


if __name__ == "__main__":
    main()
