from pages.base_page import BasePage
from locators.locators import ForgotPasswordPageLocators, LoginPageLocators


class ForgotPasswordPage(BasePage):
    def open_forgot_password_from_login(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def enter_email(self, email):
        self.input_text(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    def click_restore_button(self):
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)

    def click_show_password(self):
        self.click(ForgotPasswordPageLocators.SHOW_PASSWORD_BUTTON)

    def is_password_field_active(self):
        # Простая проверка: поле стало type="text" или получило фокус
        password_input = self.find_element(ForgotPasswordPageLocators.PASSWORD_INPUT)
        return password_input.get_attribute("type") == "text" or password_input == self.driver.switch_to.active_element
    