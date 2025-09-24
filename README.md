# Datatank – BCB PTAX Explorer

This project provides a minimal Flask application that proxies requests to the
[Banco Central do Brasil (BCB) Olinda](https://olinda.bcb.gov.br/) API and
renders a simple web interface to explore PTAX (U.S. Dollar exchange rate)
data.

## Features

- Python (Flask) backend that validates input dates and calls the BCB PTAX API.
- REST endpoint (`/api/exchange_rates`) that returns normalized JSON data.
- Single-page interface with date pickers and a dynamically populated results table.

## Getting started

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the development server:

   ```bash
   flask --app app run --debug
   ```

4. Visit http://127.0.0.1:5000/ in your browser, pick the desired date range, and
   click **Load data**. The application will request the information from the
   BCB Olinda service and display the buy/sell quotations.

> **Note:** The PTAX API requires valid date ranges (YYYY-MM-DD). If the remote
> service is unreachable, the page displays an error message describing the
> failure.

## Project structure

```
├── app.py               # Flask entry-point with API proxy routes
├── requirements.txt     # Python dependencies
├── static/
│   ├── script.js        # Front-end behaviour
│   └── styles.css       # Interface styling
└── templates/
    └── index.html       # Main HTML shell
```
