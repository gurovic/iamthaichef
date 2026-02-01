# Инструкция по конвертации данных из SQL Server в SQLite

## Проблема
Файлы `.mdf` и `.ldf` являются бинарными файлами базы данных Microsoft SQL Server. Они не могут быть напрямую прочитаны или конвертированы в SQLite без установленного SQL Server или специализированного программного обеспечения.

## Решения

### Вариант 1: Использование SQL Server Express (рекомендуется)

1. Скачайте и установите SQL Server Express (бесплатная версия):
   - https://www.microsoft.com/en-us/sql-server/sql-server-downloads

2. Установите SQL Server Management Studio (SSMS):
   - https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms

3. Подключитесь к .mdf файлу:
   - Запустите SSMS
   - Подключитесь к серверу (если устанавливали SQL Server Express, обычно это `.\SQLEXPRESS`)
   - В Object Explorer выберите "Attach" и укажите путь к .mdf файлу

4. Экспортируйте данные:
   - Сделайте Right-click на базе данных → Tasks → Generate Scripts
   - Выберите "Select specific database objects" и укажите нужные таблицы
   - В Advanced настройках выберите "Script Data" = True
   - Сохраните результат в .sql файл

5. Конвертируйте SQL Server скрипт в SQLite формат:
   - Измените синтаксис SQL под SQLite (типы данных, ограничения и т.д.)
   - Используйте инструменты конвертации или ручную правку

### Вариант 2: Использование сторонних инструментов

1. Используйте инструменты типа:
   - Full Convert (платный)
   - MySQL Workbench (имеет возможности импорта)
   - DB Browser for SQLite (импорт данных)

2. Используйте ODBC драйверы:
   - Установите ODBC драйвер для SQL Server
   - Установите ODBC драйвер для SQLite
   - Используйте инструменты для переноса данных между ODBC источниками

### Вариант 3: Программное решение с Python

```python
import pyodbc
import sqlite3
import pandas as pd

# Подключение к SQL Server
sql_server_conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=.\SQLEXPRESS;'  # или ваш сервер
    r'DATABASE=thaitree;'
    r'Trusted_Connection=yes;'
)

# Подключение к SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')

# Получение списка таблиц
tables_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
tables = pd.read_sql(tables_query, sql_server_conn)

for table in tables['TABLE_NAME']:
    print(f"Конвертация таблицы: {table}")
    df = pd.read_sql(f"SELECT * FROM {table}", sql_server_conn)
    df.to_sql(table, sqlite_conn, if_exists='replace', index=False)

# Закрытие соединений
sql_server_conn.close()
sqlite_conn.close()
```

## Замечания по конвертации

При конвертации из SQL Server в SQLite обратите внимание на:

1. **Типы данных**:
   - SQL Server: DATETIME2 → SQLite: TEXT (ISO формат даты)
   - SQL Server: NVARCHAR → SQLite: TEXT
   - SQL Server: BIT → SQLite: INTEGER (0 или 1)

2. **Ограничения**:
   - Уникальность: UNIQUE constraint
   - Внешние ключи: FOREIGN KEY constraint

3. **Автоинкремент**:
   - SQL Server: IDENTITY(1,1) → SQLite: INTEGER PRIMARY KEY AUTOINCREMENT

## Заключение

Для успешной конвертации данных из SQL Server в SQLite рекомендуется:

1. Установить SQL Server Express и SSMS
2. Подключить .mdf файл
3. Экспортировать данные в SQL формате
4. Адаптировать скрипт под синтаксис SQLite
5. Загрузить данные в SQLite базу данных Django

Альтернативно, можно использовать онлайн-конвертеры или специализированные инструменты, но они могут не всегда корректно обрабатывать сложные структуры данных.