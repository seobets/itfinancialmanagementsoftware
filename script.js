const button = document.getElementById("explainButton");
const explanation = document.getElementById("simpleExplanation");

button.addEventListener("click", function () {
  explanation.classList.toggle("hidden");

  if (explanation.classList.contains("hidden")) {
    button.textContent = "Explain this simply";
  } else {
    button.textContent = "Hide explanation";
  }
});