from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'bio', 'avatar', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        } 