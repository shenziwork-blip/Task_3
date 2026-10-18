import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user
from locators.locators import MainPageLocators

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

    @allure.title("Клик по ингредиенту открывает модальное окно")
    def test_ingredient_modal_opens(self, driver):
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.click_first_ingredient()
        # Проверяем, что модалка появилась (по крестику или заголовку)
        assert page.is_element_visible(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.title("Модальное окно закрывается по крестику")
    def test_ingredient_modal_closes(self, driver):
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.click_first_ingredient()
        page.close_modal()
        # После закрытия крестик должен исчезнуть
        assert not page.is_element_visible(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.title("При добавлении ингредиента увеличивается каунтер")
    @pytest.mark.parametrize("tab, index, expected_increase", [
        ("Булки", 0, 2),
        ("Соусы", 0, 1),
        ("Начинки", 0, 1),
    ])
    def test_ingredient_counter_increases(self, driver, tab, index, expected_increase):
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.switch_to_tab(tab)

        
        counter_before = page.get_ingredient_counter(index)
        page.add_ingredient_to_order(index)
        counter_after = page.get_ingredient_counter(index)

        assert counter_after == counter_before + expected_increase

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_user_can_create_order(self, driver):
        # Логинимся
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)
        WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

        # Переходим на главную и оформляем заказ
        page = MainPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/")
        page.switch_to_tab("Булки")
        page.add_ingredient_to_order(0)
        page.click_order_button()

        # Проверяем, что заказ создан (появилось модальное окно с номером заказа)
        assert page.is_element_visible(MainPageLocators.ORDER_MODAL)
