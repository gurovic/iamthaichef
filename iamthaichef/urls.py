"""
URL configuration for iamthaichef project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import tree.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('load-data', tree.views.load_data),
    path('bulk-load/', tree.views.bulk_load),
    path('get_tree_data/<str:dish_type>', tree.views.get_tree_data, name='get_tree_data'),
    path('dish/<int:id>/<str:dish_type>', tree.views.show_dish, name='dish'),
    path('refresh', tree.views.refresh_recipe_numbers),
    path('tree/<str:dish_type>', tree.views.show_tree, name="tree"),
    path('refresh', tree.views.refresh_recipe_numbers),
    path('', tree.views.show_tree)
]
