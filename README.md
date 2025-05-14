# Ателье одежды - Веб-приложение на Flask
Веб-приложение для ателье одежды с возможностью оформления заказов, управления статусами и авторскими проектами.

## Особенности

- Регистрация и авторизация пользователей
- Разделение ролей (клиенты и сотрудники)
- Каталог готовых моделей одежды с возможностью дополнения
- Создание авторских заказов
- Корзина и оформление заказов
- Личный кабинет с историей заказов
- Панель управления для сотрудников
- Статистика по использованию материалов

## 🛠 Технологический стек

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, Jinja2
- **База данных**: SQLite (с возможностью миграций через Flask-Migrate)
- **Дополнительно**: Flask-Login, Flask-WTF, SQLAlchemy

Дополнение: требуется создание папки ателье/instance для корректной работы программы. Автоматического создания пока нет
 

# Atelie - тесты

[![codecov](https://codecov.io/gh/IsamuYosida/Atelie/graph/badge.svg?token=79P2EDXU28)](https://codecov.io/gh/IsamuYosida/Atelie)
https://codecov.io/gh/IsamuYosida/Atelie/graphs/sunburst.svg?token=79P2EDXU28

## CI/CD Статус

Наш процесс непрерывной интеграции включает:

✅ **Автоматическое тестирование**:
- Запуск unit-тестов при каждом push/pull request
- Проверка покрытия кода (coverage)
- Интеграция с PostgreSQL

# Пример конфигурации тестов
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov=atelie

##Пока работают только тесты!!!

Запуск через app.py или
### Установка
```bash
git clone https://github.com/IsamuYosida/Atelie.git
cd Atelie
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
