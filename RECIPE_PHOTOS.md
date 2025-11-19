# Recipe Photos Feature

This document describes the recipe photos submission and approval feature.

## Overview

Users can submit photos for recipes. Admins review and approve/reject submissions. Approved photos are displayed on recipe pages with author attribution.

## User Workflow

1. **View Recipe**: Navigate to a recipe detail page by clicking on a recipe title from the dish page
2. **Submit Photo**: Click the "Suggest Photo" button (requires login)
3. **Upload Form**: 
   - Select an image file
   - Choose photo type(s):
     - Restaurant dish photo
     - Handmade photo
     - Ingredients/cooking process photo
     - Main photo
4. **Submit**: Photo is submitted with status "suggested"
5. **View Photos**: Once approved by admin, photo appears on the recipe page with your username

## Admin Workflow

1. **Access Admin Panel**: Navigate to `/admin/`
2. **View Submitted Photos**: 
   - Go to "Recipe photos" to see all submissions
   - Filter by status (suggested/approved/canceled)
   - Or edit a Recipe and see photos in the inline admin
3. **Review Photo**:
   - Change status to "approved" to make it visible to users
   - Change status to "canceled" to reject it
   - Adjust photo type flags as needed
4. **Save Changes**: Photo status is updated

## Technical Details

### Model: RecipePhoto

- `recipe`: Foreign key to Recipe
- `user`: Foreign key to User (photo author)
- `image`: ImageField storing photo file
- `status`: Choice field (suggested/approved/canceled)
- `is_restaurant_dish`: Boolean flag
- `is_handmade`: Boolean flag
- `is_ingredients_process`: Boolean flag
- `is_main_photo`: Boolean flag
- `upload_date`: Auto-set timestamp

### URLs

- `/recipe/<id>`: Recipe detail page showing approved photos
- `/recipe/<id>/suggest-photo`: Photo submission form

### Permissions

- Any authenticated user can submit photos
- Only admins can approve/reject photos
- Anonymous users can view approved photos

### Media Files

- Photos are uploaded to `media/recipe_photos/`
- Make sure `MEDIA_ROOT` and `MEDIA_URL` are properly configured
- The `media/` directory is excluded from git via `.gitignore`

## Setup

1. Install Pillow: `pip install Pillow`
2. Run migrations: `python manage.py migrate`
3. Collect static files if needed: `python manage.py collectstatic`
4. Ensure media directory exists and is writable
