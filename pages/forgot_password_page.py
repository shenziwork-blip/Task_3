from pages.base_page import BasePage
from locators.locators import ForgotPasswordPageLocators, LoginPageLocators


class ForgotPasswordPage(BasePage):
    def open_forgot_password_from_login(self):
        self.js_click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def enter_email(self, email):
        self.input_text(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    def click_restore_button(self):
        self.js_click(ForgotPasswordPageLocators.RESTORE_BUTTON)

    def click_show_password(self):
        self.js_click(ForgotPasswordPageLocators.SHOW_PASSWORD_BUTTON)

    def is_password_input_visible(self):
        return self.is_element_visible(ForgotPasswordPageLocators.PASSWORD_INPUT)

    def wait_for_password_input(self):
        self.find_element(ForgotPasswordPageLocators.PASSWORD_INPUT)

    def is_password_field_active(self):
        password_input = self.find_element(ForgotPasswordPageLocators.PASSWORD_INPUT)
        return password_input.is_displayed()