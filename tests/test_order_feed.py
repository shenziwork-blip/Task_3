import allure
from pages.order_feed_page import OrderFeedPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers.user_helper import create_user, delete_user
from constants import BASE_URL


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Клик по заказу открывает модальное окно с деталями")
    def test_order_modal_opens(self, driver):
        page = OrderFeedPage(driver)
        page.open(f"{BASE_URL}/feed")
        page.click_first_order()
        assert page.page_contains("Modal_modal__container")

    @allure.title("Заказы пользователя из Истории заказов отображаются в Ленте заказов")
    def test_user_orders_visible_in_feed(self, driver):
        email, password, token = create_user()
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(email, password)

        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.add_ingredient_to_order()
        main_page.click_order_button()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_order_modal()

        feed_page = OrderFeedPage(driver)
        feed_page.open(f"{BASE_URL}/feed")
        assert feed_page.is_order_number_ready(order_number) or feed_page.is_order_number_in_progress(order_number)

        delete_user(token)

    @allure.title("При создании нового заказа счётчик Выполнено за всё время увеличивается")
    def test_total_done_counter_increases(self, driver):
        feed_page = OrderFeedPage(driver)
        feed_page.open(f"{BASE_URL}/feed")
        before = feed_page.get_total_done_count()

        email, password, token = create_user()
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(email, password)

        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.add_ingredient_to_order()
        main_page.click_order_button()
        main_page.close_order_modal()

        feed_page.open(f"{BASE_URL}/feed")
        after = feed_page.get_total_done_count()
        assert after > before

        delete_user(token)

    @allure.title("При создании нового заказа счётчик Выполнено за сегодня увеличивается")
    def test_today_done_counter_increases(self, driver):
        feed_page = OrderFeedPage(driver)
        feed_page.open(f"{BASE_URL}/feed")
        before = feed_page.get_today_done_count()

        email, password, token = create_user()
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(email, password)

        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.add_ingredient_to_order()
        main_page.click_order_button()
        main_page.close_order_modal()

        feed_page.open(f"{BASE_URL}/feed")
        after = feed_page.get_today_done_count()
        assert after > before

        delete_user(token)

    @allure.title("После оформления заказа его номер появляется в разделе В работе")
    def test_order_number_appears_in_progress(self, driver):
        email, password, token = create_user()
        login_page = LoginPage(driver)
        login_page.open(f"{BASE_URL}/login")
        login_page.login(email, password)

        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.add_ingredient_to_order()
        main_page.click_order_button()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_order_modal()

        feed_page = OrderFeedPage(driver)
        feed_page.open(f"{BASE_URL}/feed")
        assert feed_page.wait_for_order_in_progress(order_number)

        delete_user(token)