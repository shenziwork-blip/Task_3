import allure
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage


class TestPasswordRecovery:
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_forgot_password_page(self, driver):
        page = ForgotPasswordPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/login")
        page.open_forgot_password_from_login()

        assert "forgot-password" in driver.current_url

    @allure.title("Ввод почты и клик по кнопке Восстановить")
    def test_restore_password_with_email(self, driver):
        page = ForgotPasswordPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/forgot-password")
        page.enter_email("test@yandex.ru")
        page.click_restore_button()

        # После клика обычно редирект на страницу сброса или появляется поле пароля
        assert "reset-password" in driver.current_url or page.is_element_visible(ForgotPasswordPageLocators.PASSWORD_INPUT)

    @allure.title("Кнопка показать/скрыть пароль делает поле активным")
    def test_show_hide_password_makes_field_active(self, driver):
        page = ForgotPasswordPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/reset-password")
        page.click_show_password()

        assert page.is_password_field_active()
        