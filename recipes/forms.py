from django import forms
from .models import Recipe, Comment, Rating


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'instructions', 'image', 'cooking_time')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название рецепта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание блюда'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Каждый ингредиент с новой строки\nнапр: 200г муки'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Пошаговая инструкция приготовления'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'ingredients': 'Ингредиенты',
            'instructions': 'Способ приготовления',
            'image': 'Фото блюда',
            'cooking_time': 'Время приготовления (мин)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите комментарий...'}),
        }
        labels = {'text': ''}


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score',)
        widgets = {
            'score': forms.RadioSelect(attrs={'class': 'rating-radio'}),
        }
        labels = {'score': 'Ваша оценка'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].choices = [(i, f'{"★" * i}{"☆" * (5 - i)}') for i in range(5, 0, -1)]


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или ингредиентам...',
        })
    )
