from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


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



SOURCE_TYPES = [
    ("S", "site"),
    ("B", "book"),
    ("Y", "YouTube channel"),
    ("N", "no source"),
]


class Source(models.Model):
    title = models.CharField(max_length=400)
    source_type = models.CharField(max_length=2, choices=SOURCE_TYPES, default="N")
    url = models.CharField(max_length=400, null=True, blank=True)

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
    users = models.ManyToManyField(User, through='UserRecipeRelation')

    def __str__(self):
        return f"---{self.title}--- ({self.source}, {self.subsource}) [{self.category}]"

    def ingredients_string(self):
        ingredients_alternatives = self.ingredientalternatives_set.all()
        result = []
        for alternative in ingredients_alternatives:
            if alternative.optional:
                result.append("(" + "/".join(map(Ingredient.link, alternative.ingredients.all())) + ")")
            else:
                result.append("/".join(map(Ingredient.link, alternative.ingredients.all())))
        return ", ".join(result) or ""


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


class News(models.Model):
    text = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "news"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} {self.text[:40]}..."


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ingredient_type = models.ForeignKey('IngredientType', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def link(self):
        return f"<a href='/ingredient/{self.id}'>{self.name}</a>"


class IngredientAlternatives(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    optional = models.BooleanField(default=False)

    def __str__(self):
        return ("(" if self.optional else "") + "/".join(map(str, self.ingredients.all())) + (")" if self.optional else "")


class IngredientType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class IngredientAlias(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.ingredient.name})"
