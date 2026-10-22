from pages.base_page import BasePage
from locators.locators import AccountPageLocators


class AccountPage(BasePage):
    def click_personal_account(self):
        self.js_click(AccountPageLocators.PERSONAL_ACCOUNT_LINK)

    def go_to_order_history(self):
        self.js_click(AccountPageLocators.ORDER_HISTORY_LINK)

    def logout(self):
        self.js_click(AccountPageLocators.LOGOUT_BUTTON)

    def is_on_account_page(self):
        url = self.get_current_url()
        return "account" in url or "profile" in url
    