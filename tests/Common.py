from random import randbytes
from robot.api.deco import keyword


class Common:
    def __init__(self):
        pass

    @keyword("Generate Random Username And Password")
    def generate_random_username_and_password(self) -> tuple:
        username = randbytes(8).hex()
        password = randbytes(8).hex()
        return f"{username}@quiztester.dev", password
