import allure
from pages.account_page import AccountPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user
from constants import BASE_URL


class TestAccount:
    def setup_method(self):
        self.email, self.password, self.token = create_user()

    def teardown_method(self):
        if hasattr(self, "token") and self.token:
            delete_user(self.token)

    @allure.title("Переход по клику на Личный кабинет")
    def test_go_to_personal_account(self, driver):
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(self.email, self.password)

        login_page.wait_for_url_not_contains("login")

        account_page = AccountPage(driver)
        account_page.click_personal_account()

        account_page.wait_for_url_contains("account")
        assert "account" in account_page.get_current_url()

    @allure.title("Переход в раздел История заказов")
    def test_go_to_order_history(self, driver):
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(self.email, self.password)

        login_page.wait_for_url_not_contains("login")

        account_page = AccountPage(driver)
        account_page.click_personal_account()
        account_page.go_to_order_history()

        account_page.wait_for_url_contains("order-history")
        assert "order-history" in account_page.get_current_url()

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver):
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(self.email, self.password)

        login_page.wait_for_url_not_contains("login", timeout=25)

        account_page = AccountPage(driver)
        account_page.click_personal_account()
        account_page.logout()

        account_page.wait_for_url_contains("login")
        assert "login" in account_page.get_current_url()
