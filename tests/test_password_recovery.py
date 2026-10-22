import allure
from pages.forgot_password_page import ForgotPasswordPage
from constants import BASE_URL

class TestPasswordRecovery:
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_forgot_password_page(self, driver):
        page = ForgotPasswordPage(driver)
        page.open(f"{BASE_URL}/login")
        page.open_forgot_password_from_login()

        assert "forgot-password" in page.get_current_url()

    @allure.title("Ввод почты и клик по кнопке Восстановить")
    def test_restore_password_with_email(self, driver):
        page = ForgotPasswordPage(driver)
        page.open(f"{BASE_URL}/forgot-password")
        page.enter_email("test@yandex.ru")
        page.click_restore_button()

        # После клика обычно редирект или появляется поле для нового пароля
        assert "reset-password" in page.get_current_url() or page.is_password_input_visible()

    @allure.title("Кнопка показать/скрыть пароль делает поле активным")
    def test_show_hide_password_makes_field_active(self, driver):
        page = ForgotPasswordPage(driver)
        page.open(f"{BASE_URL}/forgot-password")
        page.enter_email("test@yandex.ru")
        page.click_restore_button()

        # Ждём появления поля пароля
        page.wait_for_password_input()

        page.click_show_password()
        assert page.is_password_field_active()
