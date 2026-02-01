# Инструкция по работе с PostgreSQL через Docker и импорту данных в SQLite

## Проблема
Файлы с расширением .mdf и .ldf обычно используются Microsoft SQL Server, а не PostgreSQL. 
Если данные действительно находятся в формате PostgreSQL, они должны иметь другое расширение.

## Варианты решения

### Вариант 1: Если данные в формате SQL Server (.mdf/.ldf)

1. Установите SQL Server Express (как описано в предыдущем файле)
2. Извлеките данные в SQL формате
3. Преобразуйте SQL скрипт под PostgreSQL
4. Загрузите в PostgreSQL через Docker

### Вариант 2: Если данные в формате PostgreSQL

Для работы с PostgreSQL через Docker выполните следующие шаги:

1. Убедитесь, что у вас установлен Docker
2. Создайте файл docker-compose.yml:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: postgres_thaitree
    environment:
      POSTGRES_DB: thaitree
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: code123
    ports:
      - "5432:5432"
    volumes:
      - ./data:/var/lib/postgresql/data
      - ./import.sql:/docker-entrypoint-initdb.d/import.sql
    restart: unless-stopped
```

3. Если у вас есть дамп базы данных в формате .sql, поместите его в файл import.sql
4. Запустите контейнер:

```bash
docker-compose up -d
```

### Вариант 3: Прямой экспорт из PostgreSQL в SQLite

Если у вас есть доступ к PostgreSQL базе данных, можно использовать следующий подход:

```python
import psycopg2
import sqlite3
import pandas as pd

# Подключение к PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    database="thaitree",
    user="postgres",
    password="code123"
)

# Подключение к SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')

# Список таблиц для экспорта
tables = ['tree_news', 'tree_ingredienttype', 'tree_ingredient', 'tree_ingredientalias', 
          'tree_source', 'tree_category', 'tree_recipe', 'tree_ingredientalternatives', 
          'tree_userreciperelation']

for table in tables:
    print(f"Конвертация таблицы: {table}")
    df = pd.read_sql(f"SELECT * FROM {table}", pg_conn)
    df.to_sql(table, sqlite_conn, if_exists='replace', index=False)

pg_conn.close()
sqlite_conn.close()
```

## Для Django приложения

После импорта данных в PostgreSQL, можно настроить Django для работы с этой базой:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'thaitree',
        'USER': 'postgres',
        'PASSWORD': 'code123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Затем выполнить:
```bash
python manage.py migrate --run-syncdb
```

## Заключение

Для корректной работы с данными важно знать их точный формат. 
Если у вас есть дамп базы данных в формате .sql или доступ к работающему PostgreSQL серверу,
мы можем продолжить работу с этими данными.