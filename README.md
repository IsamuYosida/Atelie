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
 

# Atelie - Система управления ателье

![Tests](https://github.com/IsamuYosida/Atelie/actions/workflows/ci.yml/badge.svg)

## CI/CD Pipeline
Проект использует GitHub Actions для автоматизации:

### Тестирование (`ci.yml`)
- Запуск pytest с покрытием кода
- Интеграция с PostgreSQL
- Проверка всех маршрутов Flask
- Отправка отчета о покрытии в Codecov

###Пока работают только тесты!!!

Запуск через app.py или
### Установка
```bash
git clone https://github.com/IsamuYosida/Atelie.git
cd Atelie
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
