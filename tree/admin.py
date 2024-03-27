from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Dish, Variant, Source, Recipe


class CategoryAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish)
admin.site.register(Variant)
admin.site.register(Source)
admin.site.register(Recipe)
