from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


# Category 1->* ... 1->* Category -> Dish 1->*    Dish variation 1->* Recipe
# Soup ->     Without noodles -> Tom Yum -> Tom Yum Goong -> from pailin
class Category(MPTTModel):
    title = models.CharField(max_length=200)
    thai_title = models.CharField(max_length=200, blank=True, null=True)
    thai_transcript_name = models.CharField(max_length=200, blank=True, null=True)
    parent = TreeForeignKey('self',  blank=True, null=True, on_delete=models.CASCADE,
                            related_name='children')

    def __str__(self):
        return f"{self.title} #{self.id}"

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


class Recipe(models.Model):
    title = models.CharField(max_length=400)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    subsource = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"---{self.title}--- ({self.source}, {self.subsource}) [{self.category}]"
