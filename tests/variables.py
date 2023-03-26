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
