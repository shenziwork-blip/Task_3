import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class WebDriverFactory:
    @staticmethod
    def create_driver(browser_name):
        if browser_name.lower() == "chrome":
            options = ChromeOptions()
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )

        if browser_name.lower() == "firefox":
            options = FirefoxOptions()
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("media.navigator.permission.disabled", True)
            return webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )

        raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = WebDriverFactory.create_driver(request.param)
    yield browser
    browser.quit()
