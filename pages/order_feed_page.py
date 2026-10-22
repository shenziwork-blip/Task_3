from pages.base_page import BasePage
from locators.locators import OrderFeedPageLocators
from selenium.webdriver.support import expected_conditions as EC
from constants import BASE_URL


class OrderFeedPage(BasePage):
    def click_first_order(self):
        first = self.wait.until(EC.element_to_be_clickable(OrderFeedPageLocators.ORDER_ITEM))
        self.execute_script("arguments[0].click();", first)

    def get_total_done_count(self):
        return int(self.get_text(OrderFeedPageLocators.TOTAL_DONE_COUNTER))

    def get_today_done_count(self):
        return int(self.get_text(OrderFeedPageLocators.TODAY_DONE_COUNTER))

    def is_order_number_ready(self, order_number):
        try:
            clean_number = order_number.replace("#", "").strip()
            padded = clean_number.zfill(5)
            ready_section = self.find_element(OrderFeedPageLocators.READY_LIST)
            text = ready_section.text
            return clean_number in text or padded in text
        except Exception:
            return False

    def is_order_number_in_progress(self, order_number):
        try:
            clean_number = order_number.replace("#", "").strip()
            padded = clean_number.zfill(5)
            in_progress = self.find_element(OrderFeedPageLocators.IN_PROGRESS_LIST)
            text = in_progress.text.replace(" ", "").replace("\n", "")
            return clean_number in text or padded in text
        except Exception:
            return False

    def get_orders_count(self):
        return len(self.find_elements(OrderFeedPageLocators.ORDER_ITEM))

    def wait_for_order_in_progress(self, order_number, timeout=25):
        def _condition(_driver):
            if self.is_order_number_in_progress(order_number):
                return True
            self.open(f"{BASE_URL}/feed")
            return False

        try:
            self.wait_until(_condition, timeout=timeout)
            return True
        except Exception:
            return False