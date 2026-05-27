# Text Summariser

A simple, beginner-friendly Python tool that reads a block of text from a file, sends it to the [Anthropic Claude API](https://www.anthropic.com/), and writes a concise summary to an output file.

## How It Works

1. You drop your text into `input.txt`
2. The script sends it to Claude
3. The summary is saved to `summary.txt` and printed to the terminal

## Requirements

- Python 3.8+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

**1. Clone the repo and move into the folder:**

```bash
git clone https://github.com/clarkeir76/text-summariser.git
cd text-summariser
```

**2. Create a virtual environment and install dependencies:**

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your API key:**

```bash
cp .env.example .env
```

Open `.env` and replace `your-api-key-here` with your real Anthropic API key. This file is listed in `.gitignore` so it will **never** be committed to Git.

## Usage

**1. Add the text you want to summarise to `input.txt`:**

```bash
# Paste your text directly into the file, or pipe it in:
pbpaste > input.txt        # macOS: paste from clipboard
cat my-article.txt > input.txt
```

**2. Run the summariser:**

```bash
python summarise.py
```

**3. Find your summary in `summary.txt`** (it's also printed to the terminal).

## Project Structure

```
text-summariser/
├── summarise.py       # Main script
├── input.txt          # Put your text here
├── summary.txt        # Your summary appears here (created on first run)
├── requirements.txt   # Python dependencies
├── .env.example       # Template for your API key
├── .env               # Your actual API key (never committed)
└── .gitignore
```

## Security Note

Your API key lives in `.env`, which is excluded from version control by `.gitignore`. Never paste your API key directly into `summarise.py` or any other file that gets committed to Git.

## License

MIT
