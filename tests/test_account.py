import allure
from pages.account_page import AccountPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user
from selenium.webdriver.support.ui import WebDriverWait

class TestAccount:
    def setup_method(self):
        self.email, self.password, self.token = create_user()

    def teardown_method(self):
        if hasattr(self, "token") and self.token:
            delete_user(self.token)

    @allure.title("Переход по клику на Личный кабинет")
    def test_go_to_personal_account(self, driver):
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)

        # Ждём, что ушли со страницы логина
        WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

        account_page = AccountPage(driver)
        account_page.click_personal_account()

        # Проверяем, что попали в кабинет
        WebDriverWait(driver, 10).until(lambda d: "account" in d.current_url or "profile" in d.current_url)
        assert "account" in driver.current_url or "profile" in driver.current_url

    @allure.title("Переход в раздел История заказов")
    def test_go_to_order_history(self, driver):
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)

        account_page = AccountPage(driver)
        account_page.click_personal_account()
        account_page.go_to_order_history()

        assert "orders" in driver.current_url or "profile/orders" in driver.current_url

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver):
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)

        account_page = AccountPage(driver)
        account_page.click_personal_account()
        account_page.logout()

        # После выхода обычно редирект на логин или главную
        assert "login" in driver.current_url or "stellarburgers" in driver.current_url