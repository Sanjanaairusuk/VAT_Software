// Attach event listener once the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const checkBtn = document.getElementById("checkBtn");
  checkBtn.addEventListener("click", fetchVATData);
});
// Fetch VAT obligations from backend
async function fetchVATData() {
  const vatNumber = document.getElementById("vatNumber").value.trim();
  const output = document.getElementById("output");
  // Validate input
  if (!vatNumber) {
    output.textContent = "⚠️ Please enter a VAT number.";
    return;
  }
  output.textContent = "⏳ Fetching VAT obligations...";
  try {
    const BACKEND_URL =
      "https://fuzzy-chainsaw-pj5qwp67x7q4369g7-8000.app.github.dev";
    const response = await fetch(
      `${BACKEND_URL}/vat/obligations?vrn=${vatNumber}&from_date=2023-10-01&to_date=2023-12-31`
    );

    // Handle HTTP errors
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText);
    }
 const data = await response.json();
    // Display formatted JSON output
    output.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    output.textContent = `❌ Error fetching VAT data:\n${error.message}`;
  }
}
