const analyzeButton = document.getElementById("analyzeButton");
const inputField = document.getElementById("textToAnalyze");
const responseElement = document.getElementById("system_response");

async function runEmotionAnalysis() {
  const textToAnalyze = inputField.value.trim();

  if (!textToAnalyze) {
    responseElement.textContent = "Invalid text! Please try again.";
    return;
  }

  const response = await fetch(
    `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
  );
  const responseText = await response.text();
  responseElement.textContent = responseText;
}

analyzeButton.addEventListener("click", () => {
  runEmotionAnalysis().catch(() => {
    responseElement.textContent =
      "Emotion analysis service is unavailable right now.";
  });
});
