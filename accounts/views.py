from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AvatarForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    from recipes.models import Recipe
    profile = request.user.profile
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар обновлён!')
            return redirect('profile')
    else:
        form = AvatarForm(instance=profile)
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'user_recipes': user_recipes, 'avatar_form': form})
