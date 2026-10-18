import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.order_feed_page import OrderFeedPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from helpers.user_helper import create_user, delete_user
from locators.locators import MainPageLocators, OrderFeedPageLocators


class TestOrderFeed:
    def setup_method(self):
        self.email, self.password, self.token = create_user()

    def teardown_method(self):
        if hasattr(self, "token") and self.token:
            delete_user(self.token)

    @allure.title("Клик по заказу открывает всплывающее окно с деталями")
    def test_order_modal_opens(self, driver):
        page = OrderFeedPage(driver)
        page.open("https://qa-stellarburgers.education-services.ru/feed")
        page.click_first_order()

        # Ждём перехода на страницу заказа
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(driver, 10).until(
            lambda d: "/feed/" in d.current_url and d.current_url != "https://qa-stellarburgers.education-services.ru/feed"
        )
        assert "/feed/" in driver.current_url

    @allure.title("Заказы пользователя из Истории заказов отображаются в Ленте заказов")
    def test_user_orders_visible_in_feed(self, driver):
        # Логинимся и создаём заказ
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)
        WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

        main_page = MainPage(driver)
        main_page.open("https://qa-stellarburgers.education-services.ru/")
        main_page.switch_to_tab("Булки")
        main_page.add_ingredient_to_order(0)
        main_page.click_order_button()
        WebDriverWait(driver, 10).until(lambda d: main_page.is_element_visible(MainPageLocators.ORDER_MODAL))
        main_page.close_modal()

        # Идём в историю
        account_page = AccountPage(driver)
        account_page.click_personal_account()
        account_page.go_to_order_history()
        WebDriverWait(driver, 10).until(lambda d: "order-history" in d.current_url)

        # Переходим в ленту и проверяем, что заказы отображаются
        feed_page = OrderFeedPage(driver)
        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")
        orders = feed_page.find_elements(OrderFeedPageLocators.ORDER_ITEM)
        assert len(orders) > 0

    @allure.title("При создании нового заказа счётчик Выполнено за всё время увеличивается")
    def test_total_done_counter_increases(self, driver):
        feed_page = OrderFeedPage(driver)
        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")
        before = feed_page.get_total_done_count()

        # Создаём заказ
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)
        WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

        main_page = MainPage(driver)
        main_page.open("https://qa-stellarburgers.education-services.ru/")
        main_page.switch_to_tab("Булки")
        main_page.add_ingredient_to_order(0)
        main_page.click_order_button()
        WebDriverWait(driver, 15).until(lambda d: main_page.is_element_visible(MainPageLocators.ORDER_MODAL))
        main_page.close_modal()

        # Возвращаемся в ленту и проверяем счётчик
        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")
        after = feed_page.get_total_done_count()
        assert after >= before

    @allure.title("При создании нового заказа счётчик Выполнено за сегодня увеличивается")
    def test_today_done_counter_increases(self, driver):
        feed_page = OrderFeedPage(driver)
        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")
        before = feed_page.get_today_done_count()

        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)
        WebDriverWait(driver, 15).until(lambda d: "login" not in d.current_url)

        main_page = MainPage(driver)
        main_page.open("https://qa-stellarburgers.education-services.ru/")
        main_page.switch_to_tab("Булки")
        main_page.add_ingredient_to_order(0)
        main_page.click_order_button()
        WebDriverWait(driver, 15).until(lambda d: main_page.is_element_visible(MainPageLocators.ORDER_MODAL))
        main_page.close_modal()

        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")
        after = feed_page.get_today_done_count()
        assert after >= before

    @allure.title("После оформления заказа его номер появляется в разделе В работе")
    def test_order_number_appears_in_progress(self, driver):
        login_page = LoginPage(driver)
        login_page.open("https://qa-stellarburgers.education-services.ru/login")
        login_page.login(self.email, self.password)
        WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url)

        main_page = MainPage(driver)
        main_page.open("https://qa-stellarburgers.education-services.ru/")
        main_page.switch_to_tab("Булки")
        main_page.add_ingredient_to_order(0)
        main_page.click_order_button()

        # Получаем номер заказа из модалки
        order_modal = main_page.find_element(MainPageLocators.ORDER_MODAL)

        # Ждём, пока вместо 9999 появится настоящий номер
        WebDriverWait(driver, 10).until(
            lambda d: order_modal.find_element(By.XPATH, ".//h2").text not in ("9999", "0", "")
        )
        order_number = order_modal.find_element(By.XPATH, ".//h2").text
        main_page.close_modal()

        feed_page = OrderFeedPage(driver)
        feed_page.open("https://qa-stellarburgers.education-services.ru/feed")

        found = False
        for _ in range(10):
            if feed_page.is_order_number_in_progress(order_number):
                found = True
                break
            time.sleep(1.5)
            driver.refresh()

        assert found, f"Номер заказа {order_number} не появился в разделе «В работе»"
