"""
Скрипт для конвертации данных из SQL Server в SQLite
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path

def convert_sqlserver_to_sqlite(sqlserver_db_path, sqlite_db_path):
    """
    Конвертирует базу данных SQL Server в SQLite
    """
    try:
        # Попытка подключения к SQL Server файлу через pymssql или pyodbc
        # Так как прямой доступ к .mdf файлу ограничен без установленного SQL Server,
        # будем использовать альтернативный подход
        
        print("Попытка конвертации данных...")
        
        # Подключение к целевой SQLite базе данных
        conn_sqlite = sqlite3.connect(sqlite_db_path)
        cursor_sqlite = conn_sqlite.cursor()
        
        # Создание таблиц в SQLite (структура должна совпадать с моделями Django)
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS tree_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text VARCHAR(500) NOT NULL,
            date DATE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_ingredienttype (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) UNIQUE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_ingredient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) UNIQUE NOT NULL,
            ingredient_type_id INTEGER REFERENCES tree_ingredienttype(id)
        );
        
        CREATE TABLE IF NOT EXISTS tree_ingredientalias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) UNIQUE NOT NULL,
            ingredient_id INTEGER REFERENCES tree_ingredient(id)
        );
        
        CREATE TABLE IF NOT EXISTS tree_source (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(400) NOT NULL,
            source_type VARCHAR(2) NOT NULL,
            url VARCHAR(400) NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            thai_title VARCHAR(200) NULL,
            thai_transcript_name VARCHAR(200) NULL,
            parent_id INTEGER REFERENCES tree_category(id),
            number_of_recipes INTEGER DEFAULT 0,
            number_of_veg_recipes INTEGER DEFAULT 0,
            number_of_fish_recipes INTEGER DEFAULT 0,
            number_of_seafood_recipes INTEGER DEFAULT 0,
            lft INTEGER NOT NULL,
            rght INTEGER NOT NULL,
            tree_id INTEGER NOT NULL,
            level INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_recipe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(400) NOT NULL,
            source_id INTEGER NOT NULL REFERENCES tree_source(id),
            subsource VARCHAR(400) NOT NULL,
            link VARCHAR(400) NOT NULL,
            category_id INTEGER NOT NULL REFERENCES tree_category(id),
            vegetarian VARCHAR(2) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS auth_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(128) NOT NULL,
            email VARCHAR(254) NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_userreciperelation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES auth_user(id),
            recipe_id INTEGER NOT NULL REFERENCES tree_recipe(id),
            cooked VARCHAR(1) NOT NULL,
            tasted VARCHAR(1) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_ingredientalternatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL REFERENCES tree_recipe(id),
            optional BOOLEAN NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS tree_ingredientalternatives_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredientalternatives_id INTEGER NOT NULL REFERENCES tree_ingredientalternatives(id),
            ingredient_id INTEGER NOT NULL REFERENCES tree_ingredient(id)
        );
        """
        
        cursor_sqlite.executescript(create_tables_sql)
        conn_sqlite.commit()
        
        print("Структура таблиц создана в SQLite базе данных.")
        
        # Закрытие соединений
        conn_sqlite.close()
        
        print(f"SQLite база данных создана: {sqlite_db_path}")
        print("Теперь вам нужно импортировать данные из SQL Server в SQLite.")
        print("Это может потребовать использования SQL Server Management Studio или других инструментов.")
        
    except Exception as e:
        print(f"Ошибка при конвертации: {str(e)}")
        print("Возможно, вам нужно установить дополнительные драйверы для работы с SQL Server.")

if __name__ == "__main__":
    # Определение путей к файлам
    sqlserver_mdf_path = r"C:\Users\Fablab\Downloads\thaitree.mdf"
    sqlite_db_path = r"C:\Users\Fablab\iamthaichef\db.sqlite3"
    
    # Проверка существования файлов
    if not os.path.exists(sqlserver_mdf_path):
        print(f"Файл {sqlserver_mdf_path} не найден!")
    else:
        print(f"Найден файл SQL Server: {sqlserver_mdf_path}")
        convert_sqlserver_to_sqlite(sqlserver_mdf_path, sqlite_db_path)