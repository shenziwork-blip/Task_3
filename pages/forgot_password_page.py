from pages.base_page import BasePage
from locators.locators import ForgotPasswordPageLocators, LoginPageLocators


class ForgotPasswordPage(BasePage):
    def open_forgot_password_from_login(self):
        link = self.find_element(LoginPageLocators.FORGOT_PASSWORD_LINK)
        self.driver.execute_script("arguments[0].click();", link)

    def enter_email(self, email):
        self.input_text(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    def click_restore_button(self):
        button = self.find_element(ForgotPasswordPageLocators.RESTORE_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)

    def click_show_password(self):
        btn = self.find_element(ForgotPasswordPageLocators.SHOW_PASSWORD_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_password_field_active(self):
        password_input = self.find_element(ForgotPasswordPageLocators.PASSWORD_INPUT)
        # Проверяем, что поле видимо и имеет фокус или type изменился
        return password_input.is_displayed()
    
    