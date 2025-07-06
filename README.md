# Django Табель учёта сотрудников

Простая система табельного учёта на Django: добавление сотрудников, учёт рабочего времени, отчёты, экспорт в Excel.  
Подойдёт для малого бизнеса или учебного проекта.

---

## Возможности

- Регистрация / авторизация пользователей
- Учёт рабочего времени сотрудников (табели)
- Просмотр и редактирование профиля
- Отчёты по отработанным часам и сменам
- CRUD для сотрудников
- Экспорт данных в Excel

---

## Скриншоты

- Главная страница неавторизованного пользователя  
 ![Скриншот Главной страницы](https://github.com/Ryota77777/TabApp/blob/main/templates/main.jpg?raw=true)

- Дашборд после входа  
  ![Скриншот дашборда](https://github.com/Ryota77777/TabApp/blob/main/templates/dash.png?raw=true)

- Список табелей  
  ![Скриншот табелей](https://github.com/Ryota77777/TabApp/blob/main/templates/tabel.png?raw=true)

- Список сотрудников  
  ![Скриншот списка сотрудников](https://github.com/Ryota77777/TabApp/blob/main/templates/employee.png?raw=true)

- Отчёты по часам  
  ![Скриншот отчетов](https://github.com/Ryota77777/TabApp/blob/main/templates/otcheti.png?raw=true)

- Профиль и настройки сотрудника  
  ![Скриншот настроек и профиля](https://github.com/Ryota77777/TabApp/blob/main/templates/settings.png?raw=true)

---

## Установка

> Python 3.9+ и Django 4.2+ должны быть установлены

1. Клонируем репозиторий:

```bash
git clone https://github.com/Ryota77777/TabApp.git
cd TabApp
```

2.Устанавливаем зависимости:
```bash
pip install -r requirements.txt
```
3.Создаём базу данных и применяем миграции:
```bash
python manage.py migrate
```
4.Запускаем сервер:
```bash
python manage.py runserver
```
5.Открываем в браузере:
http://127.0.0.1:8000/

---

## Лицензия
MIT
Автор: [Ryota77777]

---
