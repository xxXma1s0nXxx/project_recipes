from django.contrib import admin
from .models import Recipe, Favorite, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time', 'created_at')
    search_fields = ('title', 'ingredients')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'score')


admin.site.register(Favorite)
