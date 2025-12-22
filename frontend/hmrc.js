function continueToHMRC() {
  // Redirect to FastAPI HMRC OAuth endpoint
  window.location.href = "http://localhost:8000/authorize";
}

function goBack() {
  window.history.back();
}
