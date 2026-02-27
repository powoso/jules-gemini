# Social Media Scraper App

A simple full-stack application that scrapes posts from **Reddit** and **Twitter** (via Nitter mirror `xcancel.com`) and displays them in a unified feed.

## Features

- **Unified Feed**: View posts from both Reddit (r/technology) and Twitter (@elonmusk) in one place.
- **Source Filtering**: Toggle between viewing All, Reddit only, or Twitter only.
- **Clean UI**: Modern, dark-mode interface built with Tailwind CSS.
- **Responsive**: Works on desktop and mobile.

## Tech Stack

- **Backend**: Python, FastAPI
- **Scraping**: `requests` (Reddit RSS), `playwright` (Twitter/XCancel)
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN)

## Quick Start (MacOS/Linux)

We have provided a helper script to setup the environment and run the app easily.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/powoso/jules-gemini.git
    cd social-media-scraper
    ```
    *(Note: If the directory name after cloning is different, `cd` into that directory)*

2.  **Run the Setup & Start Script**:
    This script will create a virtual environment, install dependencies, and start the server.
    ```bash
    chmod +x run.sh
    ./run.sh
    ```

3.  **Open the App**:
    Once the server starts, open your browser and go to: `http://localhost:8000`

---

## Manual Installation

If you prefer to run commands manually:

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright Browsers**:
    Required for the Twitter scraper.
    ```bash
    playwright install chromium
    ```

4.  **Run the App**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Troubleshooting "Command not found"

If you see errors like `zsh: command not found: pip` or `playwright`, it usually means you aren't inside the virtual environment.

- **Ensure you have Python installed**: Run `python3 --version`. If not, install it via `brew install python` (on Mac).
- **Activate the environment**: Run `source venv/bin/activate`. You should see `(venv)` in your terminal prompt.
- **Run with python module**: Instead of `uvicorn`, try `python3 -m uvicorn app.main:app --reload`.

## Testing

You can run the included tests using `pytest`:

```bash
# Run unit tests
PYTHONPATH=. pytest tests/test_scrapers.py

# Verify frontend via Playwright script
python3 verify_frontend.py
```
