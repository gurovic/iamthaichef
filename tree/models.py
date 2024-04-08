from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
# Create your models here.


# Category 1->* ... 1->* Category -> Dish 1->*    Dish variation 1->* Recipe
# Soup ->     Without noodles -> Tom Yum -> Tom Yum Goong -> from pailin
class Category(MPTTModel):
    title = models.CharField(max_length=200)
    thai_title = models.CharField(max_length=200, blank=True, null=True)
    thai_transcript_name = models.CharField(max_length=200, blank=True, null=True)
    parent = TreeForeignKey('self',  blank=True, null=True, on_delete=models.CASCADE,
                            related_name='children')
    number_of_recipes = models.IntegerField(default=0)
    number_of_veg_recipes = models.IntegerField(default=0)
    number_of_fish_recipes = models.IntegerField(default=0)
    number_of_seafood_recipes = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.title} #{self.id} " +  (self.thai_title or "") +
                ("/" if self.thai_title and self.thai_transcript_name else "") + (self.thai_transcript_name or "") +
                (f" <{self.number_of_recipes} recipe" if self.number_of_recipes > 0 else "") +
                ("s>" if self.number_of_recipes > 1 else ">" if self.number_of_recipes > 0 else ""))

    class Meta:
        verbose_name_plural = "categories"


# Source (Book, site...) 1<----through recipe_source---* Recipe *->1 Category
#                              subsource (page, link...)
# Variant 1<-* Recipe


SOURCE_TYPES = [
    ("S", "site"),
    ("B", "book"),
    ("N", "no source"),
]


class Source(models.Model):
    title = models.CharField(max_length=400)
    source_type = models.CharField(max_length=2, choices=SOURCE_TYPES, default="N")

    def __str__(self):
        return self.title


VEG_TYPES = [
    ("V", "vegetarian"),
    ("F", "with fish"),
    ("S", "with seafood"),
    ("M", "with meat"),
    ("?", "no info")
]


class Recipe(models.Model):
    title = models.CharField(max_length=400)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    subsource = models.CharField(max_length=400)
    link = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vegetarian = models.CharField(max_length=2, choices=VEG_TYPES, default="?")
    ingredients = models.CharField(max_length=400, null=True, blank=True, default="")

    def __str__(self):
        return f"---{self.title}--- ({self.source}, {self.subsource}) [{self.category}]"

COOK_STATUS = [
    ("N", "Never cooked"),
    ("W", "Want to cook"),
    ("C", "Cooked"),
    ("S", "My signature dish"),
]

TASTE_STATUS = [
    ("N", "Never tasted"),
    ("W", "Want to taste"),
    ("T", "Tasted"),
    ("F", "My favorite dish"),
]
class UserRecipeRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cooked = models.CharField(max_length=1, choices=COOK_STATUS, default="N")
    tasted = models.CharField(max_length=1, choices=TASTE_STATUS, default="N")


    def __str__(self):
        return f"{self.user} - {self.recipe.title}"

class News (models.Model):
    text = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "news"
        ordering = ["-date"]


    def __str__(self):
        return f"{self.date} {self.text[:40]}..."
