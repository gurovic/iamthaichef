from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Source, Recipe, UserRecipeRelation


class CategoryAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Source)
admin.site.register(Recipe)
admin.site.register(UserRecipeRelation)
