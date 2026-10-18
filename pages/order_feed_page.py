from pages.base_page import BasePage
from locators.locators import OrderFeedPageLocators
from selenium.webdriver.common.action_chains import ActionChains
import time


class OrderFeedPage(BasePage):
    def click_first_order(self):
        orders = self.find_elements(OrderFeedPageLocators.ORDER_ITEM)
        if orders:
            first = orders[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first)
            time.sleep(0.7)
            ActionChains(self.driver).move_to_element(first).click().perform()

    def get_total_done_count(self):
        return int(self.get_text(OrderFeedPageLocators.TOTAL_DONE_COUNTER))

    def get_today_done_count(self):
        return int(self.get_text(OrderFeedPageLocators.TODAY_DONE_COUNTER))

    def is_order_number_in_progress(self, order_number):
        try:
            items = self.find_elements(OrderFeedPageLocators.IN_PROGRESS_LIST + (By.TAG_NAME, "li"))
            # Альтернативный простой вариант:
            section = self.find_element(OrderFeedPageLocators.IN_PROGRESS_LIST)
            clean_number = order_number.replace("#", "").strip()
            return clean_number in section.text
        except Exception:
            return False

    def is_order_number_ready(self, order_number):
        try:
            from selenium.webdriver.common.by import By
            clean_number = order_number.replace("#", "").strip()
            padded = clean_number.zfill(5)
            ready_section = self.find_element((By.XPATH, "//p[text()='Готовы:']/following-sibling::ul"))
            text = ready_section.text
            return clean_number in text or padded in text
        except Exception:
            return False

    def is_order_number_in_progress(self, order_number):
        try:
            from selenium.webdriver.common.by import By
            clean_number = order_number.replace("#", "").strip()
            padded = clean_number.zfill(5)
            in_progress = self.find_element((By.XPATH, "//p[contains(text(), 'В работе')]/following-sibling::ul"))
            text = in_progress.text.replace(" ", "").replace("\n", "")
            return clean_number in text or padded in text
        except Exception:
            return False
        