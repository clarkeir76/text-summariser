"""
Text Summariser
===============
Reads text from input.txt, sends it to the OpenAI API,
and writes a concise summary to summary.txt.

Usage:
  1. Copy .env.example to .env and add your OpenAI API key
  2. Add the text you want to summarise to input.txt
  3. Run:  python summarise.py
  4. Find your summary in summary.txt
"""

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env (keeps your API key out of the code)
load_dotenv()


def read_input(file_path: str) -> str:
    """Read text from a file and return it as a string."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find '{file_path}'.\n"
            "Please create the file and add the text you want to summarise."
        )


def write_output(file_path: str, content: str) -> None:
    """Write content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def summarise(text: str) -> str:
    """Send text to OpenAI and return a concise summary."""

    # The OpenAI client automatically reads OPENAI_API_KEY from the environment
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Please provide a clear, concise summary of the following text. "
                    "Capture the key points and main ideas in a few short paragraphs.\n\n"
                    f"{text}"
                ),
            }
        ],
    )

    return response.choices[0].message.content or ""


def main() -> None:
    input_file = "input.txt"
    output_file = "summary.txt"

    print(f"📖  Reading text from '{input_file}'...")
    text = read_input(input_file)

    if not text:
        print("⚠️   The input file is empty. Please add some text and try again.")
        return

    word_count = len(text.split())
    print(f"✅  Read {word_count} words.")

    print("🤖  Sending to OpenAI for summarisation...")
    summary = summarise(text)

    print(f"💾  Writing summary to '{output_file}'...")
    write_output(output_file, summary)

    print("\n✨  Done! Here's your summary:\n")
    print("-" * 60)
    print(summary)
    print("-" * 60)


if __name__ == "__main__":
    main()
