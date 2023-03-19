from robot.api.deco import keyword
from selenium import webdriver


class Selenium:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-crash-reporter')
        self.options.add_argument('--remote-debugging-port=9222')

    @keyword("Get Chrome Options")
    def get_chrome_options(self):
        return self.options
