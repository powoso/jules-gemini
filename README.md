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

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd social-media-scraper
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Install Playwright Browsers**:
    Required for the Twitter scraper to work.
    ```bash
    playwright install chromium
    ```

## Running the App

1.  **Start the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Open the App**:
    Navigate to `http://localhost:8000` in your web browser.

## Testing

You can run the included tests using `pytest`:

```bash
# Run unit tests
PYTHONPATH=. pytest tests/test_scrapers.py

# Verify frontend via Playwright script
python3 verify_frontend.py
```

## Notes

- The Twitter scraper relies on `xcancel.com`, a Nitter instance. If this instance goes down or changes its structure, the Twitter feed may stop working. You can update the URL in `app/services/twitter.py` if needed.
- Reddit scraping uses the public RSS feeds which are subject to rate limits.
