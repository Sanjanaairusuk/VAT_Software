const API_BASE_URL = "https://test-api.service.hmrc.gov.uk/organisations/vat";

async function fetchVATData() {
  const vatNumber = document.getElementById("vatNumber").value.trim();
  const output = document.getElementById("output");

  if (!vatNumber) {
    output.textContent = "⚠️ Please enter a VAT number.";
    return;
  }

  output.textContent = "⏳ Fetching VAT obligations...";

  try {
    const response = await fetch(`${API_BASE_URL}/vat/obligations`, {
      headers: {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN", // replace with your token
        "Accept": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status} ${response.statusText}`);
    }

    // Try parsing as JSON, fallback to text
    let data;
    const contentType = response.headers.get("content-type");

    if (contentType && contentType.includes("application/json")) {
      data = await response.json();
      output.textContent = JSON.stringify(data, null, 2);
    } else {
      data = await response.text();
      output.textContent = data;
    }

  } catch (error) {
    output.textContent = "❌ Error fetching VAT obligations: " + error.message;
  }
}
