from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Recipe, Favorite, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm, SearchForm


def home(request):
    recipes = Recipe.objects.select_related('author').all()
    search_form = SearchForm(request.GET)
    query = ''
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '')
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) | Q(ingredients__icontains=query)
            )
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )
    return render(request, 'recipes/home.html', {
        'recipes': recipes,
        'search_form': search_form,
        'query': query,
        'favorite_ids': favorite_ids,
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.select_related('user').all()
    comment_form = CommentForm()
    rating_form = RatingForm()
    user_rating = None
    is_favorite = False

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
        if user_rating:
            rating_form = RatingForm(instance=user_rating)
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
    })


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт успешно создан!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Новый рецепт'})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт обновлён!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Редактировать рецепт', 'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Рецепт удалён.')
        return redirect('home')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        fav.delete()
        messages.info(request, 'Рецепт удалён из избранного.')
    else:
        messages.success(request, 'Рецепт добавлен в избранное!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def favorites(request):
    fav_recipes = Recipe.objects.filter(favorited_by__user=request.user).select_related('author')
    return render(request, 'recipes/favorites.html', {'recipes': fav_recipes})


@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
    return redirect('recipe_detail', pk=pk)


@login_required
def add_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        existing = Rating.objects.filter(user=request.user, recipe=recipe).first()
        form = RatingForm(request.POST, instance=existing)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            messages.success(request, 'Оценка сохранена!')
    return redirect('recipe_detail', pk=pk)
