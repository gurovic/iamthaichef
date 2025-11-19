import difflib
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login

from .forms import LoginForm, UserRegistrationForm, RecipePhotoForm
from . import spreadsheet
from .models import (Category, Recipe, News, UserRecipeRelation, Ingredient, IngredientAlternatives,
                     IngredientType, IngredientAlias, RecipePhoto)


# this view was used once to transfer ingredients from one-string format to db
def upgrade_ingredients(request):
    recipes = Recipe.objects.all()
    for recipe in recipes:
        ingredients_str = str(recipe.ingredients)
        ingredients_alternatives_list = list(map(str.strip, ingredients_str.split(',')))
        for alternative in ingredients_alternatives_list:
            optional = 0
            if alternative and alternative[0] == "(" and alternative[-1] == ")":
                optional = 1
                alternative = alternative[1:-1]
            ingredients = list(map(str.strip, alternative.split('/')))
            ingredient_objects = []
            for ingredient in ingredients:
                try:
                    ingredient_obj = Ingredient.objects.get(name=ingredient)
                except:
                    ingredient_obj = Ingredient(name=ingredient)
                    ingredient_obj.save()
                ingredient_objects.append(ingredient_obj)
            ia = IngredientAlternatives(dishes=recipe, optional=optional)
            ia.save()
            ia.ingredients.set(ingredient_objects)

    return redirect('/')


def get_tree_data(request, dish_type):
    tree_data = []
    if dish_type == "M":
        objects = Category.objects.all()
    elif dish_type == "V":
        objects = Category.objects.filter(Q(number_of_veg_recipes__gt=0))
    elif dish_type == "F":
        objects = Category.objects.filter(Q(number_of_fish_recipes__gt=0) | Q(number_of_veg_recipes__gt=0))
    else:
        objects = Category.objects.filter(Q(number_of_seafood_recipes__gt=0) |
                                          Q(number_of_fish_recipes__gt=0) |
                                          Q(number_of_veg_recipes__gt=0))

    for obj in objects:
        if dish_type == "M":
            count = obj.number_of_recipes
        elif dish_type == "V":
            count = obj.number_of_veg_recipes
        elif dish_type == "F":
            count = obj.number_of_fish_recipes + obj.number_of_veg_recipes
        else:
            count = obj.number_of_seafood_recipes + obj.number_of_fish_recipes + obj.number_of_veg_recipes

        tree_data.append({
            'id': obj.id,
            'parent': obj.parent_id if obj.parent else '#',  # '#' points to root level
            'text': f"{obj.title} ({count})",
            'a_attr': {'href': f'/dish/{obj.id}/{dish_type}'}
        })

    return JsonResponse(tree_data, safe=False)


def load_data(request):
    return render(request, 'load_data.html')


@require_http_methods(["GET"])
def bulk_load(request):
    # column 3 -> recipe.source
    # column 4 -> recipe.subsource
    # column 5 -> recipe.link
    # column 6 -> recipe.title

    # column 7 -> recipe.category (new)
    # column 8 -> recipe.category.thai_title
    # column 9 -> recipe.category.thai_transcription_name
    # column 11 -> recipe.category.parent

    # column 14 -> INGREDIENTS model
    for line in spreadsheet.get_data(request.GET['start_line'], request.GET['finish_line']):
        # line[11](L) != "" or line[7](H) == "-"
        if line[7] != '-':
            category = Category(title=line[7],
                                thai_title=line[8],
                                thai_transcript_name=line[9],
                                parent_id=int(line[11]))
            category.save()
        else:
            category = Category.objects.get(pk=int(line[11]))

        # line[6](G) != "" and line[3](D) != "" and line[14](O) != "" and line[17](R) != ""
        recipe = Recipe(title=line[6],
                        source_id=int(line[3]),
                        subsource=line[4],
                        link=line[5],
                        category=category,
                        # TODO refactor for new model
                        ingredients=line[14],
                        vegetarian=line[17])
        recipe.save()

    return redirect('/')

def prepare_data(request):
    return render(request, 'prepare_data.html')


def bulk_prepare(request):
    if request.method == "GET":
        new_ingredients = []
        ingredients = Ingredient.objects.all().values_list('name', flat=True)
        ingredient_objects = Ingredient.objects.all()
        ingredients_aliases = IngredientAlias.objects.all().values_list('name', flat=True)
        categories = IngredientType.objects.all()
        for line in spreadsheet.get_data(request.GET['start_line'], request.GET['finish_line']):
            data : str = line[14].replace('.', ',').lower()
            ingredient_alternatives = list(map(str.strip, data.split(',')))
            for alternative in ingredient_alternatives:
                alternative = alternative.replace("(", "")
                alternative = alternative.replace(")", "")
                if alternative and alternative[0] == "(":
                    alternative = alternative[1:-1]
                new_ingredients += alternative.split('/')

        aliases = list()
        alias_names = list()
        print(list(ingredients) + list(ingredients_aliases))
        for new_ingredient in set(new_ingredients):
            if new_ingredient not in list(ingredients) + list(ingredients_aliases):
                suggestions = difflib.get_close_matches(new_ingredient, ingredients)
                alias_names += [new_ingredient]
                aliases += [{'name': new_ingredient, "variants": suggestions}]
        return render(request, 'choose_aliases.html', {'aliases': aliases,
                                                       'alias_names': alias_names,
                                                       'ingredient_objects': ingredient_objects,
                                                       'categories': categories})
    else:
        aliases = request.POST["alias_names"]
        print(aliases)
        for alias_name in aliases.replace('[','').replace(']','').split(', '):
            alias_name = alias_name.strip("'")
            if alias_name in request.POST:
                if request.POST[alias_name] == 'other':
                    IngredientAlias(name=alias_name, ingredient_id=int(request.POST[alias_name+"_other"])).save()
                elif request.POST[alias_name] == 'other_id':
                    IngredientAlias(name=alias_name, ingredient_id=int(request.POST[alias_name+"_other_id"])).save()
                elif request.POST[alias_name] == 'new':
                    ingredient = Ingredient(name=request.POST[alias_name + "_new"],
                                            ingredient_type=IngredientType.objects.get(pk=request.POST[alias_name + "_type"]))
                    ingredient.save()
                    IngredientAlias(name=alias_name, ingredient=ingredient).save()
                else:    # new alias
                    IngredientAlias(name=alias_name, ingredient=Ingredient.objects.get(name=request.POST[alias_name])).save()
        return redirect('/')


def show_tree(request, dish_type="M"):
    return render(request, "NiceAdmin/index.html", {'categories': Category.objects.all(),
                                                    'dish_type': dish_type,
                                                    'news': News.objects.all()})


def show_dish(request, id, dish_type):
    dish = Category.objects.get(pk=id)
    if dish_type == "M":
        recipes = dish.recipe_set.all()
    elif dish_type == "V":
        recipes = dish.recipe_set.filter(Q(vegetarian='V'))
    elif dish_type == "F":
        recipes = dish.recipe_set.filter(Q(vegetarian='V') | Q(vegetarian='F'))
    else:
        recipes = dish.recipe_set.filter(Q(vegetarian='V') | Q(vegetarian='F') | Q(vegetarian='S'))

    if not request.user.is_anonymous:
        for recipe in recipes:
            cooked = UserRecipeRelation.objects.filter(user=request.user, recipe=recipe).values('cooked')
            if cooked:
                recipe.cooked = cooked[0]['cooked']
            else:
                recipe.cooked = 'N'
    return render(request, 'NiceAdmin/dish_page.html', {'dish': dish, 'recipes': recipes})


def recipe_number(cat):
    result = len(cat.recipe_set.all())
    result_v = len(cat.recipe_set.filter(vegetarian="V"))
    result_f = len(cat.recipe_set.filter(vegetarian="F"))
    result_s = len(cat.recipe_set.filter(vegetarian="S"))
    for child in cat.children.all():
        result += recipe_number(child)[0]
        result_v += recipe_number(child)[1]
        result_f += recipe_number(child)[2]
        result_s += recipe_number(child)[3]
    cat.number_of_recipes = result
    cat.number_of_veg_recipes = result_v
    cat.number_of_fish_recipes = result_f
    cat.number_of_seafood_recipes = result_s
    cat.save()
    return result, result_v, result_f, result_s


def refresh_recipe_numbers(request):
    cats = Category.objects.filter(parent=None)
    for cat in cats:
        recipe_number(cat)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def select_cooked(request, recipe_id, cooked):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.users.remove(request.user)
    recipe.users.add(request.user, through_defaults={"cooked": cooked})
    recipe.save()
    return HttpResponse()


def user_recipes(request, dish_type):
    recipes = request.user.userreciperelation_set.all()
    return render(request, 'NiceAdmin/user_recipes.html', {'dish_type': dish_type, 'user_recipes': recipes})


def ingredient_dishes(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    print(1, ingredient.name)
    alternatives = IngredientAlternatives.objects.filter(ingredients=ingredient_id)
    recipes = []
    for alternative in alternatives:
        recipes.append(alternative.recipe)
    return render(request, 'NiceAdmin/ingredient_recipes.html', {'ingredient': ingredient, 'recipes': recipes})


def ingredient_list(request):
    ingredient_types = IngredientType.objects.all()
    result = dict()
    for obj in ingredient_types:
        ingredients = Ingredient.objects.filter(ingredient_type=obj).order_by('name')
        result[obj] = ingredients
    return render(request, 'NiceAdmin/ingredients_list.html', {'ingredients': result})


def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def recipe_detail(request, recipe_id):
    from django.shortcuts import get_object_or_404
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    approved_photos = recipe.photos.filter(status='approved')
    
    if not request.user.is_anonymous:
        cooked = UserRecipeRelation.objects.filter(user=request.user, recipe=recipe).values('cooked')
        if cooked:
            recipe.cooked = cooked[0]['cooked']
        else:
            recipe.cooked = 'N'
    
    return render(request, 'NiceAdmin/recipe_detail.html', {
        'recipe': recipe,
        'photos': approved_photos
    })


def suggest_recipe_photo(request, recipe_id):
    from django.shortcuts import get_object_or_404
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if request.user.is_anonymous:
        return redirect('/login/')
    
    if request.method == 'POST':
        form = RecipePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.recipe = recipe
            photo.user = request.user
            photo.status = 'suggested'
            photo.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipePhotoForm()
    
    return render(request, 'NiceAdmin/suggest_photo.html', {
        'form': form,
        'recipe': recipe
    })
