"""
Скрипт для загрузки данных в Django-приложение после конвертации из SQL Server в SQLite
"""
import os
import django
import sys
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iamthaichef.settings')
django.setup()

from tree.models import News, Ingredient, IngredientType, Source, Category, Recipe, IngredientAlias, IngredientAlternatives, UserRecipeRelation

def load_data_from_sqlite():
    """
    Загружает данные в Django модели из SQLite базы данных
    """
    print("Начинаем загрузку данных в Django модели...")
    
    # Пример загрузки данных (в реальности данные будут уже в базе после конвертации)
    # Здесь мы просто проверяем, что структура работает
    
    # Создание тестового пользователя, если он не существует
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print("Создан суперпользователь: admin/adminpass")
    
    # Подсчет количества записей в основных моделях
    print(f"Количество новостей: {News.objects.count()}")
    print(f"Количество типов ингредиентов: {IngredientType.objects.count()}")
    print(f"Количество ингредиентов: {Ingredient.objects.count()}")
    print(f"Количество источников: {Source.objects.count()}")
    print(f"Количество категорий: {Category.objects.count()}")
    print(f"Количество рецептов: {Recipe.objects.count()}")
    print(f"Количество псевдонимов ингредиентов: {IngredientAlias.objects.count()}")
    print(f"Количество альтернатив ингредиентов: {IngredientAlternatives.objects.count()}")
    print(f"Количество связей пользователь-рецепт: {UserRecipeRelation.objects.count()}")
    
    print("Загрузка данных завершена!")

if __name__ == "__main__":
    load_data_from_sqlite()