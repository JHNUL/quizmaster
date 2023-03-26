from random import randbytes, choice
from robot.api.deco import keyword


class Common:
    def __init__(self):
        pass

    @keyword("Generate Random Username And Password")
    def generate_random_username_and_password(self) -> tuple:
        username = randbytes(8).hex()
        password = randbytes(8).hex()
        return f"{username}@quiztester.dev", password

    @keyword("Get Random Element From List")
    def get_random_element_from_list(self, elements: list):
        return choice(elements)
