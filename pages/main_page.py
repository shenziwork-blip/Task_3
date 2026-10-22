from pages.base_page import BasePage
from locators.locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.current_tab = "Булки"

    def click_constructor(self):
        self.js_click(MainPageLocators.CONSTRUCTOR_BUTTON)

    def click_order_feed(self):
        self.js_click(MainPageLocators.ORDER_FEED_BUTTON)

    def click_first_ingredient(self):
        ingredients = self.find_elements(MainPageLocators.INGREDIENT_ITEM)
        if ingredients:
            self.execute_script("arguments[0].click();", ingredients[0])

    def close_modal(self):
        self.js_click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON))

    def get_ingredient_counter(self, index=0):
        ingredients = self.get_ingredients_in_current_tab()
        counter = self.find_child(ingredients[index], MainPageLocators.INGREDIENT_COUNTER)
        return int(counter.text)

    def get_ingredients_in_current_tab(self):
        locator = (
            MainPageLocators.TAB_INGREDIENTS[0],
            MainPageLocators.TAB_INGREDIENTS[1].format(self.current_tab)
        )
        return self.find_elements(locator)

    def click_order_button(self):
        self.wait.until(EC.presence_of_element_located(MainPageLocators.ORDER_BUTTON))
        self.js_click(MainPageLocators.ORDER_BUTTON)

    def add_ingredient_to_order(self, index=0):
        if not getattr(self, "current_tab", None):
            self.current_tab = "Булки"
        ingredients = self.get_ingredients_in_current_tab()
        ingredient = ingredients[index]
        drop_zone = self.find_element(MainPageLocators.DROP_ZONE)

        self.execute_script("""
            arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});
        """, ingredient)

        self.wait.until(lambda d: ingredient.is_displayed() and drop_zone.is_displayed())

        if self.get_browser_name() == "firefox":
            self.execute_script("""
                function createEvent(type) {
                    var event = document.createEvent('HTMLEvents');
                    event.initEvent(type, true, true);
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) { this.data[type] = val; },
                        getData: function(type) { return this.data[type]; }
                    };
                    return event;
                }
                var dragStart = createEvent('dragstart');
                var drop = createEvent('drop');
                var dragEnd = createEvent('dragend');
                arguments[0].dispatchEvent(dragStart);
                arguments[1].dispatchEvent(drop);
                arguments[0].dispatchEvent(dragEnd);
            """, ingredient, drop_zone)
        else:
            self.drag_and_drop(ingredient, drop_zone)

    def get_order_number_from_modal(self):
        locator = MainPageLocators.ORDER_NUMBER_IN_MODAL
        self.wait_until(
            lambda _driver: (
                (text := self.get_text(locator).strip())
                and text != "9999"
                and text.isdigit()
            ),
            timeout=20,
        )
        return self.find_element(locator).text.strip()

    def switch_to_tab(self, tab_name):
        tab_locator = (
            MainPageLocators.TAB_BY_NAME[0],
            MainPageLocators.TAB_BY_NAME[1].format(tab_name)
        )
        tab = self.find_element(tab_locator)
        try:
            tab.click()
        except Exception:
            self.execute_script("arguments[0].click();", tab)

        self.current_tab = tab_name
        ingredients_locator = (
            MainPageLocators.TAB_INGREDIENTS[0],
            MainPageLocators.TAB_INGREDIENTS[1].format(tab_name)
        )
        self.wait.until(EC.presence_of_element_located(ingredients_locator))

    def is_modal_open(self):
        return self.is_element_visible(MainPageLocators.MODAL_CLOSE_BUTTON)

    def is_order_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)  

    def close_order_modal(self):
        self.close_modal()  