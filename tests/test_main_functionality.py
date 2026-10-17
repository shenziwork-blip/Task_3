import allure
from selenium.webdriver.support.ui import WebDriverWait
from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user


class TestMainFunctionality:
    def setup_method(self):
        self.email, self.password, self.token = create_user()

    def teardown_method(self):
        if hasattr(self, "token") and self.token:
            delete_user(self.token)

    @allure.title("Переход по клику на Конструктор")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.click_constructor()
        assert driver.current_url.rstrip("/") == "https://qa-stellarburgers.education-services.ru"

    @allure.title("Переход по клику на Лента заказов")
    def test_go_to_order_feed(self, driver):
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.click_order_feed()
        WebDriverWait(driver, 10).until(lambda d: "feed" in d.current_url)
        assert "feed" in driver.current_url
        