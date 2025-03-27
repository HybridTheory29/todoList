from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']