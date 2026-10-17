from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.locators import MainPageLocators


class MainPage(BasePage):
    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)

    def click_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_BUTTON)

    def click_first_ingredient(self):
        ingredients = self.find_elements(MainPageLocators.INGREDIENT_ITEM)
        if ingredients:
            self.driver.execute_script("arguments[0].click();", ingredients[0])

    def close_modal(self):
        close_btn = self.find_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.driver.execute_script("arguments[0].click();", close_btn)
        # Ждём, пока модалка исчезнет
        from selenium.webdriver.support import expected_conditions as EC
        self.wait.until(EC.invisibility_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON))

    def get_ingredient_counter(self):
        counter = self.find_element(MainPageLocators.INGREDIENT_COUNTER)
        return counter.text

    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)
