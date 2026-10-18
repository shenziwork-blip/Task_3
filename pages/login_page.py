from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):
    def login(self, email, password):
        self.input_text(LoginPageLocators.EMAIL_INPUT, email)
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        button = self.find_element(LoginPageLocators.LOGIN_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)
