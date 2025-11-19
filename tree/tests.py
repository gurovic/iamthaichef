from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Source, Recipe, RecipePhoto


class RecipePhotoModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test category
        self.category = Category.objects.create(title='Test Category')
        
        # Create test source
        self.source = Source.objects.create(title='Test Source', source_type='S')
        
        # Create test recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            source=self.source,
            subsource='Page 1',
            link='http://example.com',
            category=self.category,
            vegetarian='V'
        )

    def test_recipe_photo_creation(self):
        """Test that a RecipePhoto can be created"""
        photo = RecipePhoto.objects.create(
            recipe=self.recipe,
            user=self.user,
            status='suggested',
            is_main_photo=True
        )
        
        self.assertEqual(photo.recipe, self.recipe)
        self.assertEqual(photo.user, self.user)
        self.assertEqual(photo.status, 'suggested')
        self.assertTrue(photo.is_main_photo)
        
    def test_recipe_photo_default_status(self):
        """Test that RecipePhoto has default status of 'suggested'"""
        photo = RecipePhoto.objects.create(
            recipe=self.recipe,
            user=self.user
        )
        
        self.assertEqual(photo.status, 'suggested')
        
    def test_recipe_photos_relationship(self):
        """Test the relationship between Recipe and RecipePhoto"""
        photo1 = RecipePhoto.objects.create(
            recipe=self.recipe,
            user=self.user,
            status='approved'
        )
        photo2 = RecipePhoto.objects.create(
            recipe=self.recipe,
            user=self.user,
            status='suggested'
        )
        
        self.assertEqual(self.recipe.photos.count(), 2)
        
        approved_photos = self.recipe.photos.filter(status='approved')
        self.assertEqual(approved_photos.count(), 1)
        self.assertEqual(approved_photos.first(), photo1)
