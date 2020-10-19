from django import forms
from .models import Book

class Book_add(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'date_of_public': forms.SelectDateWidget(years=range(1700,2025),)

        }

