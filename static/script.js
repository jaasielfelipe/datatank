const form = document.getElementById("search-form");
const statusEl = document.getElementById("status");
const table = document.getElementById("results-table");
const tbody = table.querySelector("tbody");

const formatNumber = (value) => {
  if (typeof value !== "number") return "–";
  return value.toLocaleString(undefined, {
    minimumFractionDigits: 4,
    maximumFractionDigits: 4,
  });
};

const setLoading = (isLoading) => {
  const button = form.querySelector("button");
  button.disabled = isLoading;
  statusEl.textContent = isLoading ? "Loading data from Banco Central do Brasil…" : "";
};

const renderRows = (records) => {
  tbody.innerHTML = "";

  if (!records.length) {
    statusEl.textContent = "No data returned for the selected period.";
    table.hidden = true;
    return;
  }

  records.forEach((entry) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${entry.date ?? "–"}</td>
      <td>${formatNumber(entry.buy)}</td>
      <td>${formatNumber(entry.sell)}</td>
    `;
    tbody.appendChild(row);
  });

  statusEl.textContent = `Loaded ${records.length} quotation${records.length === 1 ? "" : "s"}.`;
  table.hidden = false;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const startDate = data.get("start-date");
  const endDate = data.get("end-date");

  setLoading(true);

  try {
    const response = await fetch(
      `/api/exchange_rates?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`
    );

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Unexpected error");
    }

    renderRows(payload.records ?? []);
  } catch (error) {
    statusEl.textContent = error.message;
    table.hidden = true;
  } finally {
    setLoading(false);
  }
});

const today = new Date();
const lastWeek = new Date();
lastWeek.setDate(today.getDate() - 7);

document.getElementById("start-date").value = lastWeek.toISOString().slice(0, 10);
document.getElementById("end-date").value = today.toISOString().slice(0, 10);
