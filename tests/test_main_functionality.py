import allure
import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user
from constants import BASE_URL


class TestMainFunctionality:
    def setup_method(self):
        self.email, self.password, self.token = create_user()

    def teardown_method(self):
        if hasattr(self, "token") and self.token:
            delete_user(self.token)

    @allure.title("Переход по клику на Конструктор")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.click_constructor()
        assert page.get_current_url().rstrip("/") == BASE_URL

    @allure.title("Переход по клику на Лента заказов")
    def test_go_to_order_feed(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.click_order_feed()
        page.wait_for_url_contains("feed")
        assert "feed" in page.get_current_url()

    @allure.title("Клик по ингредиенту открывает модальное окно")
    def test_ingredient_modal_opens(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.click_first_ingredient()
        assert page.is_modal_open()

    @allure.title("Модальное окно закрывается по крестику")
    def test_ingredient_modal_closes(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.click_first_ingredient()
        page.close_modal()
        assert not page.is_modal_open()

    @allure.title("При добавлении ингредиента увеличивается каунтер")
    @pytest.mark.parametrize("tab, index, expected_increase", [
        ("Булки", 0, 2),
        ("Соусы", 0, 1),
        ("Начинки", 0, 1),
    ])
    def test_ingredient_counter_increases(self, driver, tab, index, expected_increase):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.switch_to_tab(tab)

        counter_before = page.get_ingredient_counter(index)
        page.add_ingredient_to_order(index)
        counter_after = page.get_ingredient_counter(index)

        assert counter_after == counter_before + expected_increase

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_logged_user_can_create_order(self, driver):
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(self.email, self.password)
        login_page.wait_for_url_not_contains("login")

        page = MainPage(driver)
        page.open(BASE_URL)
        page.switch_to_tab("Булки")
        page.add_ingredient_to_order(0)
        page.click_order_button()

        assert page.is_order_modal_visible()