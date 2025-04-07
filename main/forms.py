from django import forms
from .models import *
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_time'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']