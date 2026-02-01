import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Проверяем, какие таблицы созданы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Созданные таблицы:')
for table in tables:
    print(f'  - {table[0]}')

# Проверим количество записей в каждой таблице
for table in tables:
    if table[0] not in ['sqlite_sequence']:  # исключаем системную таблицу
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'    Записей в {table[0]}: {count}')

conn.close()