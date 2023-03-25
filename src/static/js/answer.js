document.addEventListener("DOMContentLoaded", () => {
  const getAnswerCount = () => {
    const answers = document.querySelectorAll("#answeropts input");
    return answers.length;
  };

  const addAnswerBtn = document.querySelector("#add_answeropt");
  const answerOptsContainer = document.querySelector("#answeropts");
  addAnswerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    const index = getAnswerCount() + 1;
    if (index >= 6) return;
    const label = document.createElement("label");
    label.textContent = `Answer option ${index}`;
    label.setAttribute("for", `answeropt${index}`);
    const input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("name", `answeropt${index}`);
    input.setAttribute("id", `answeropt${index}`);
    input.setAttribute("autocomplete", "off");
    answerOptsContainer.appendChild(label);
    answerOptsContainer.appendChild(input);
  });
});
