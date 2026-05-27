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

# Read the .env file and inject its values into the environment,
# so OPENAI_API_KEY is available without hardcoding it in the script
load_dotenv()


def read_input(file_path: str) -> str:
    """Read text from a file and return it as a string."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # strip() removes any leading/trailing whitespace or blank lines
            return f.read().strip()
    except FileNotFoundError:
        # The file doesn't exist — give the user a clear action to take
        raise FileNotFoundError(
            f"Could not find '{file_path}'.\n"
            "Please create the file and add the text you want to summarise."
        )
    except PermissionError:
        # The file exists but the OS is blocking read access
        raise PermissionError(
            f"Could not read '{file_path}'.\n"
            "Please check that you have read permission for this file."
        )
    except UnicodeDecodeError:
        # The file contains bytes that aren't valid UTF-8 — likely a binary
        # file or a file saved in a different encoding (e.g. Latin-1)
        raise UnicodeDecodeError(
            "utf-8", b"", 0, 1,
            f"Could not read '{file_path}' as UTF-8 text.\n"
            "Please ensure the file is saved as UTF-8 and does not contain binary data."
        )
    except OSError as e:
        # Catch-all for other I/O errors (disk issues, file is a directory, etc.)
        raise OSError(
            f"Could not read '{file_path}': {e}"
        )


def write_output(file_path: str, content: str) -> None:
    """Write content to a file."""
    try:
        # "w" mode creates the file if it doesn't exist, or overwrites it if it does
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except PermissionError:
        # The OS is blocking write access to this location
        raise PermissionError(
            f"Could not write to '{file_path}'.\n"
            "Please check that you have write permission in this directory."
        )
    except OSError as e:
        # Catch-all for other I/O errors (disk full, invalid path, etc.)
        raise OSError(
            f"Could not write to '{file_path}': {e}"
        )


def summarise(text: str) -> str:
    """Send text to OpenAI and return a concise summary."""

    # The OpenAI client automatically reads OPENAI_API_KEY from the environment,
    # which was loaded from .env by load_dotenv() above
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast and cost-effective model for summarisation
        max_tokens=1024,       # cap the summary length at roughly 750 words
        messages=[
            {
                "role": "user",
                "content": (
                    "Please provide a clear, concise summary of the following text. "
                    "Capture the key points and main ideas in a few short paragraphs.\n\n"
                    f"{text}"  # the text to summarise is appended to the prompt
                ),
            }
        ],
    )

    # The API returns a list of choices — we only requested one, so take the first.
    # .content can theoretically be None, so fall back to an empty string.
    return response.choices[0].message.content or ""


def main() -> None:
    input_file = "input.txt"
    output_file = "summary.txt"

    print(f"📖  Reading text from '{input_file}'...")
    text = read_input(input_file)

    # No point calling the API if the file is empty
    if not text:
        print("⚠️   The input file is empty. Please add some text and try again.")
        return

    # Count words by splitting on whitespace — gives a rough size indicator
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


# Only run main() if this script is executed directly (e.g. python summarise.py).
# If someone imports this file into another script, main() won't fire automatically.
if __name__ == "__main__":
    main()
