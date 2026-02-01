import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iamthaichef.settings')
django.setup()

from tree.models import News, Ingredient, Recipe, Category, IngredientType

# Подсчет записей
print(f'Новостей: {News.objects.count()}')
print(f'Ингредиентов: {Ingredient.objects.count()}')
print(f'Типов ингредиентов: {IngredientType.objects.count()}')
print(f'Рецептов: {Recipe.objects.count()}')
print(f'Категорий: {Category.objects.count()}')

# Показать несколько примеров
print("\nПримеры новостей:")
for news in News.objects.all()[:5]:
    print(f"- {news.date}: {news.text}")

print("\nПримеры ингредиентов:")
for ingredient in Ingredient.objects.all()[:5]:
    print(f"- {ingredient.name}")

print("\nПримеры рецептов:")
for recipe in Recipe.objects.all()[:5]:
    print(f"- {recipe.title}")