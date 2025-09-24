"""Flask application exposing a simple interface for the BCB Olinda API."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BCB_API_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
)


class InvalidDateError(ValueError):
    """Raised when the user submits an invalid date."""


def _format_date(date_str: str) -> str:
    """Return the Olinda-compatible representation of an ISO date string."""

    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise InvalidDateError("Dates must follow the YYYY-MM-DD format.") from exc
    return parsed.strftime("%m-%d-%Y")


@app.route("/")
def index() -> str:
    """Render the front-end shell that interacts with the API."""

    return render_template("index.html")


@app.route("/api/exchange_rates")
def exchange_rates() -> Any:
    """Return a JSON payload with dollar quotation data for the requested period."""

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return (
            jsonify({
                "error": "Both start_date and end_date query parameters are required.",
            }),
            400,
        )

    try:
        formatted_start = _format_date(start_date)
        formatted_end = _format_date(end_date)
    except InvalidDateError as exc:
        return jsonify({"error": str(exc)}), 400

    params = {
        "@dataInicial": f"'{formatted_start}'",
        "@dataFinalCotacao": f"'{formatted_end}'",
        "$format": "json",
        "$orderby": "dataHoraCotacao",
    }

    try:
        response = requests.get(BCB_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network failure
        return (
            jsonify(
                {
                    "error": "Failed to retrieve data from the Banco Central do Brasil service.",
                    "details": str(exc),
                }
            ),
            502,
        )

    payload: Dict[str, Any] = response.json()
    records: List[Dict[str, Any]] = payload.get("value", [])

    normalized: List[Dict[str, Any]] = [
        {
            "date": item.get("dataHoraCotacao"),
            "buy": item.get("cotacaoCompra"),
            "sell": item.get("cotacaoVenda"),
        }
        for item in records
    ]

    return jsonify({"records": normalized})


if __name__ == "__main__":
    app.run(debug=True)
