from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image', 'location', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your ad...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Add location'}),
            'title': forms.TextInput(attrs={'placeholder': 'Add title'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Set price'})
        } 