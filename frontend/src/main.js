const API_BASE_URL = "https://test-api.service.hmrc.gov.uk/organisations/vat";

async function fetchVATData() {
  const vatNumber = document.getElementById("vatNumber").value;
  const output = document.getElementById("output");

  if (!vatNumber) {
    output.textContent = "Please enter a VAT number.";
    return;
  }

  output.textContent = "Fetching data...";

  const fromDate = "2025-01-01";
  const toDate = "2025-12-31";

  try {
    const response = await fetch(`${API_BASE_URL}/${vatNumber}/obligations?from=${fromDate}&to=${toDate}`, {
      headers: {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);

  } catch (error) {
    output.textContent = "Error fetching VAT obligations: " + error.message;
  }
}
