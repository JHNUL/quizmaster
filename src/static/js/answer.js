document.addEventListener("DOMContentLoaded", () => {
  const getAnswerCount = () => {
    const answers = document.querySelectorAll("#answeropts input[type=text]");
    return answers.length;
  };

  const addAnswerBtn = document.querySelector("#add_answeropt");
  const answerOptsContainer = document.querySelector("#answeropts");
  addAnswerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    const index = getAnswerCount() + 1;
    if (index >= 6) return;
    const span = document.createElement("span");
    span.setAttribute("id", `answer_option${index}`);
    span.innerHTML = `
      <label class="block mb-1 md:mb-0 pr-4" for="answeropt${index}">
        Answer option ${index}
      </label>
      <div class="md:flex md:items-center mb-6">
        <div class="md:w-11/12">
          <input
            class="text-input"
            type="text"
            name="answeropt${index}"
            id="answeropt${index}"
            autocomplete="off"
            required
          />
        </div>
        <div class="md:w-1/12 flex items-center justify-center">
          <input
            type="checkbox"
            id="iscorrect${index}"
            name="iscorrect"
            value="answeropt${index}"
          />
        </div>
      </div>
    `;
    answerOptsContainer.appendChild(span);
  });
});
