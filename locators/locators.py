from selenium.webdriver.common.by import By


class MainPageLocators:
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']/ancestor::a")
    INGREDIENT_ITEM = (By.XPATH, "//a[contains(@class, 'BurgerIngredient')]")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    CONSTRUCTOR_AREA = (By.XPATH, "//span[contains(text(), 'Перетяните булочку сюда')]")
    ORDER_NUMBER_IN_MODAL = (By.CSS_SELECTOR, "h2.Modal_modal__title_shadow__3ikwq")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "p.counter_counter__num__3nue1")
    DROP_ZONE = (By.CSS_SELECTOR, "section.BurgerConstructor_basket__29Cd7")
    TAB_BY_NAME = (By.XPATH, "//span[text()='{}']/parent::div")
    TAB_INGREDIENTS = (By.XPATH, "//h2[text()='{}']/following-sibling::ul[1]//a[contains(@class, 'BurgerIngredient_ingredient')]")
    ORDER_NUMBER_HEADER = (By.XPATH, ".//h2")

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[text()='Восстановить пароль']")


class ForgotPasswordPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @type='text']")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon') or contains(@class, 'input_icon')]")


class AccountPageLocators:
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/account') and contains(text(), 'Профиль')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[@href='/account/order-history']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//p[text()='Личный Кабинет']/ancestor::a")


class OrderFeedPageLocators:
    ORDER_ITEM = (By.XPATH, "//a[contains(@class, 'OrderHistory_link') and contains(@href, '/feed/')]")
    TOTAL_DONE_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_DONE_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    READY_LIST = (By.XPATH, "//p[text()='Готовы:']/following-sibling::ul")
    IN_PROGRESS_LIST = (By.XPATH, "//p[contains(text(), 'В работе')]/following-sibling::ul")