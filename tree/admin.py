from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import (Category, Source, Recipe, UserRecipeRelation, News, Ingredient, IngredientAlternatives,
                     IngredientType, IngredientAlias, RecipePhoto)


class CategoryAdmin(DjangoMpttAdmin):
    pass


class RecipePhotoInline(admin.TabularInline):
    model = RecipePhoto
    extra = 0
    readonly_fields = ('user', 'upload_date')
    fields = ('image', 'user', 'status', 'is_restaurant_dish', 'is_handmade', 
              'is_ingredients_process', 'is_main_photo', 'upload_date')


class RecipePhotoAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'status', 'is_main_photo', 'upload_date')
    list_filter = ('status', 'is_main_photo', 'is_restaurant_dish', 'is_handmade', 'is_ingredients_process')
    search_fields = ('recipe__title', 'user__username')
    readonly_fields = ('upload_date',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipePhotoInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Source)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserRecipeRelation)
admin.site.register(News)
admin.site.register(Ingredient)
admin.site.register(IngredientAlternatives)
admin.site.register(IngredientType)
admin.site.register(IngredientAlias)
admin.site.register(RecipePhoto, RecipePhotoAdmin)
