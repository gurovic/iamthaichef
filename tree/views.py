from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .models import Category, Recipe
from . import spreadsheet

def load_data(request):
    return render(request, 'load_data.html')
@require_http_methods(["GET"])
def bulk_load(request):
    # column 3 -> recipe.source
    # column 4 -> recipe.subsource
    # column 6 -> recipe.title

    # column 7 -> recipe.category (new)
    # column 8 -> recipe.category.thai_title
    # column 9 -> recipe.category.thai_transcription_name
    # column 11 -> recipe.category.parent
    for line in spreadsheet.get_data(request.GET['start_line'], request.GET['finish_line']):
        category = Category(title=line[7],
                            thai_title=line[8],
                            thai_transcript_name=line[9],
                            parent_id=int(line[11]))
        category.save()

        recipe = Recipe(title=line[6],
                        source_id=int(line[3]),
                        subsource=line[4],
                        category=category)
        recipe.save()

    return redirect('/')

def show_tree(request):
    return render(request, "tree.html", {'categories': Category.objects.all()})