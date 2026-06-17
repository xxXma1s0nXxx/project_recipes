from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('recipe/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('recipe/<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('favorites/', views.favorites, name='favorites'),
]
