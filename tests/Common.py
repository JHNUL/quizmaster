# pylint: disable=invalid-name
from random import randbytes, choice, randint
from re import match
from faker import Faker
from requests import post, Session
from robot.api.deco import keyword
from variables import ROUTES_DICT


class Common:
    def __init__(self):
        self.faker = Faker()

    def _get_cookie(self, username: str, password: str):
        data = {"username": username, "password": password}
        login_url = ROUTES_DICT["Login"]
        session = Session()
        login_res = session.post(login_url, data, timeout=3, allow_redirects=False)
        if login_res.status_code != 302:
            raise ValueError(
                f"Status code should have been 302, was {login_res.status_code}"
            )
        return session.cookies.get_dict()

    @keyword("Generate Random Username And Password")
    def generate_random_username_and_password(self) -> tuple:
        username = randbytes(8).hex()
        password = randbytes(8).hex()
        return f"{username}@quiztester.dev", password

    @keyword("Get Random Element From List")
    def get_random_element_from_list(self, elements: list):
        return choice(elements)

    @keyword("Create User")
    def create_user(self):
        username, password = self.generate_random_username_and_password()
        data = {"username": username, "password": password}
        url = ROUTES_DICT["Register"]
        res = post(url, data, timeout=3, allow_redirects=False)
        if res.status_code != 302:
            raise ValueError(f"Status code should have been 302, was {res.status_code}")
        return username, password

    @keyword("Create Quiz With Api")
    def create_quiz_with_api(
        self, username: str, password: str, questions=5, publish=True
    ):
        quiz = {}
        quiz_data = {
            "quiztitle": self.faker.text(max_nb_chars=60),
            "quizdescription": self.faker.text(max_nb_chars=250),
            "publish": publish,
        }
        quiz["quiz_title"] = quiz_data["quiztitle"]
        quiz["quiz_description"] = quiz_data["quizdescription"]
        cookie = self._get_cookie(username, password)
        url = ROUTES_DICT["Quiz"]
        res = post(url, quiz_data, timeout=3, cookies=cookie)
        if res.status_code != 200 or match(".+/quiz/\d+", res.url) is None:
            raise ValueError(
                f"Unable to create quiz, status {res.status_code}, {res.text}"
            )
        quiz_id = res.url.split("/")[-1].strip()
        quiz["quiz_id"] = quiz_id
        quiz["questions"] = []
        question_url = f"{ROUTES_DICT['Quiz']}/{quiz_id}/question"
        for _i in range(questions):
            question_data = {
                "questionname": f"{self.faker.text(max_nb_chars=60)}?",
                "answeropt1": self.faker.text(max_nb_chars=60),
                "answeropt2": self.faker.text(max_nb_chars=60),
                "answeropt3": self.faker.text(max_nb_chars=60),
                "answeropt4": self.faker.text(max_nb_chars=60),
                "answeropt5": self.faker.text(max_nb_chars=60),
                "iscorrect": f"answeropt{randint(1,5)}",
            }
            quiz["questions"].append(question_data)
            question_res = post(
                question_url,
                question_data,
                allow_redirects=False,
                timeout=3,
                cookies=cookie,
            )
            if question_res.status_code != 302:
                raise ValueError(
                    f"Unable to create question, status {question_res.status_code}, {question_res.text}"
                )

        return quiz

    @keyword("Get Quiz Id From Url")
    def get_quiz_id_from_url(self, url: str):
        return url.split("/")[-1].strip()

    @keyword("Map List Of Dictionaries To Value")
    def map_list_of_dictionaries_to_value(self, coll: list, key: str):
        return [elem[key] for elem in coll]
