from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.locators import MainPageLocators
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
        self.current_tab = "Булки"
    
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
        self.wait.until(EC.invisibility_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON))

    def get_ingredient_counter(self, index=0):
        ingredients = self.get_ingredients_in_current_tab()
        counter = ingredients[index].find_element(By.CSS_SELECTOR, "p.counter_counter__num__3nue1")
        return int(counter.text)

    def get_ingredients_in_current_tab(self):
        # Берём ингредиенты по тексту вкладки, на которую только что переключились
        return self.driver.find_elements(
            By.XPATH,
            f"//h2[text()='{self.current_tab}']/following-sibling::ul[1]//a[contains(@class, 'BurgerIngredient_ingredient')]"
        )

    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    def add_ingredient_to_order(self, index=0):
        ingredients = self.get_ingredients_in_current_tab()
        ingredient = ingredients[index]
        drop_zone = self.find_element((By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7"))

        self.driver.execute_script("""
            arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});
        """, ingredient)

        import time
        time.sleep(0.7)

        if self.driver.name == "firefox":
            self.driver.execute_script("""
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
            ActionChains(self.driver).drag_and_drop(ingredient, drop_zone).perform()

    def switch_to_tab(self, tab_name):
        tab = self.find_element((By.XPATH, f"//span[text()='{tab_name}']/parent::div"))
        # Обычный клик + JS-клик для надёжности в Firefox
        try:
            tab.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", tab)
        
        self.current_tab = tab_name
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//h2[text()='{tab_name}']/following-sibling::ul[1]//a")
        ))
