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

## Структура:
##atelier/
##├── app/
##│   ├── __init__.py       # Инициализация приложения
##│   ├── routes.py         # Маршруты Flask
##│   ├── models.py         # Модели базы данных
##│   ├── extensions.py     # Расширения Flask
##│   ├── templates/        # Шаблоны Jinja2
##│   └── static/           # Статические файлы (CSS, JS)
##├── migrations/           # Миграции базы данных
##├── instance/             # Файлы экземпляра (база данных)
##├── config.py             # Конфигурация приложения
##├── requirements.txt      # Зависимости Python
##└── README.md             # Этот файл

Запуск через app.py или
### Установка
```bash
git clone https://github.com/IsamuYosida/Atelie.git
cd Atelie
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
