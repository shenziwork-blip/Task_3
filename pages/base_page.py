from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_child(self, parent, locator):
        return parent.find_element(*locator)

    def wait_until(self, condition, timeout=20):
        return WebDriverWait(self.driver, timeout).until(condition)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def js_click(self, locator):
        element = self.find_element(locator)
        self.execute_script("arguments[0].click();", element)

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=15):
        WebDriverWait(self.driver, timeout).until(lambda d: text in d.current_url)

    def wait_for_url_not_contains(self, text, timeout=15):
        WebDriverWait(self.driver, timeout).until(lambda d: text not in d.current_url)

    def page_contains(self, text):
        return text in self.driver.page_source

    def scroll_to_element(self, element):
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def get_browser_name(self):
        return self.driver.name

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def move_to_element_and_click(self, element):
        ActionChains(self.driver).move_to_element(element).click().perform()