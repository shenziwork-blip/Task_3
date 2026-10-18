# Task 3: UI-тесты для Stellar Burgers

Автотесты веб-приложения Stellar Burgers на Python (pytest + Selenium + Allure).

## Структура проекта

- `pages/` — Page Object классы
- `locators/` — локаторы элементов
- `tests/` — тесты, разделённые по функциональности
- `helpers/` — вспомогательные функции (создание пользователей через API и т.д.)
- `conftest.py` — фикстуры и Factory для браузеров

## Запуск тестов

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt