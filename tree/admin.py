from django.contrib import admin
from .models import Category, Dish, Variant, Source, Recipe


admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Variant)
admin.site.register(Source)
admin.site.register(Recipe)
