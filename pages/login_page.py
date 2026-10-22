from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):
    def login(self, email, password):
        self.input_text(LoginPageLocators.EMAIL_INPUT, email)
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        self.js_click(LoginPageLocators.LOGIN_BUTTON)
        self.wait.until(lambda d: "login" not in d.current_url)
