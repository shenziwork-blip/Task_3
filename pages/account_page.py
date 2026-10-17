from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.locators import AccountPageLocators


class AccountPage(BasePage):
    def click_personal_account(self):
        account_link = self.find_element((By.XPATH, "//p[text()='Личный Кабинет']/ancestor::a"))
        self.driver.execute_script("arguments[0].click();", account_link)

    def go_to_order_history(self):
        link = self.find_element(AccountPageLocators.ORDER_HISTORY_LINK)
        self.driver.execute_script("arguments[0].click();", link)

    def logout(self):
        button = self.find_element(AccountPageLocators.LOGOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)

    def is_on_account_page(self):
        return "account" in self.driver.current_url or "profile" in self.driver.current_url