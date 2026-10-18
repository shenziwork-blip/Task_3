Task 3: UI-тесты для Stellar Burgers
Автотесты веб-приложения Stellar Burgers на Python (pytest + Selenium + Allure).

Структура проекта

pages/ — Page Object классы
locators/ — локаторы элементов
tests/ — тесты, разделённые по функциональности
helpers/ — вспомогательные функции (создание пользователей через API)
conftest.py — фикстуры и Factory для браузеров

Запуск тестов

Создать и активировать виртуальное окружение:
python3 -m venv .venv
source .venv/bin/activate

Установить зависимости:
pip install -r requirements.txt

Запустить все тесты:
pytest tests/ -v

Запустить тесты с Allure-результатами:
pytest tests/ --alluredir=allure-results

Сгенерировать Allure-отчёт:
allure generate allure-results -o allure-report --clean

Отчёт доступен в allure-report/index.html.