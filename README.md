# CSV to SQL Server Loader

Автоматическая загрузка нескольких CSV-файлов в Microsoft SQL Server.

## 📌 Что делает скрипт

- Сканирует папку с CSV-файлами
- Автоматически создаёт таблицы в SQL Server на основе структуры CSV
- Загружает данные в соответствующие таблицы
- Выводит статистику загрузки (сколько строк загружено)

## 🛠️ Технологии

- Python 3.x
- pandas — работа с CSV
- SQLAlchemy + pyodbc — подключение к SQL Server

## 🚀 Как запустить

### 1. Установите зависимости

```bash
pip install pandas pyodbc sqlalchemy```

**2. Настройте подключение**

В файле SQL_Integration.py измените:

DB_NAME — имя вашей базы данных

CSV_FOLDER — путь к папке с CSV-файлами

**3. Запустите скрипт**

bash
python SQL_Integration.py

**📊 Пример вывода**

Проверка подключения к SQL Server...
✅ Подключение успешно!

Найдено CSV файлов: 9
==================================================
  Загрузка olist_customers_dataset.csv...
    ✅ olist_customers_dataset: 99441 строк
  Загрузка olist_orders_dataset.csv...
    ✅ olist_orders_dataset: 99441 строк
...
==================================================
Готово! Успешно загружено: 9 из 9

**📁 Исходные данные**
Датасет: Brazilian E-Commerce Public Dataset by Olist

**Автор**
Артём Низямов
