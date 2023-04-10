document.addEventListener("DOMContentLoaded", () => {
  const getAnswerCount = () => {
    const answers = document.querySelectorAll("span[id^='answer_option']");
    return answers ? answers.length : 0;
  };
  const answerOptsContainer = document.querySelector("#answeropts");
  const addQuestionForm = document.querySelector("#add_question_form");
  const addQuestionBtn = document.querySelector("#add_question");
  const doneBtn = document.querySelector("#finish_creation");
  const cancelQuestionBtn = document.querySelector("#cancel_question");
  const addAnswerBtn = document.querySelector("#add_answeropt");
  const removeAnswerBtn = document.querySelector("#remove_answeropt");

  addQuestionBtn.addEventListener("click", (event) => {
    event.preventDefault();
    addQuestionBtn.style["display"] = "none";
    doneBtn.style["display"] = "none";
    addQuestionForm.style["display"] = "block";
  });

  addAnswerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    const index = getAnswerCount() + 1;
    if (index > 5) return;
    const span = document.createElement("span");
    span.setAttribute("id", `answer_option${index}`);
    span.innerHTML = `
      <label class="block md:mb-0 pr-4" for="answeropt${index}">
        Answer option ${index}
      </label>
      <div class="md:flex md:items-center mt-1">
        <div class="md:w-11/12">
          <input
            class="text-input"
            type="text"
            name="answeropt${index}"
            id="answeropt${index}"
            autocomplete="off"
            maxlength="100"
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

  removeAnswerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    const answers = document.querySelectorAll("span[id^='answer_option']");
    if (answers && answers.length > 2) {
      answers[answers.length - 1].remove();
    }
  });

  cancelQuestionBtn.addEventListener("click", (event) => {
    event.preventDefault();
    addQuestionForm.reset();
    const answers = document.querySelectorAll("span[id^='answer_option']");
    if (answers && answers.length > 2) {
      for (let i = 2; i < answers.length; i++) {
        answers[i].remove();
      }
    }
    addQuestionForm.style["display"] = "none";
    addQuestionBtn.style["display"] = "inline-block";
    doneBtn.style["display"] = "inline-block";
  });
});
