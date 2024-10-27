from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, DailyCheckIn

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['profile_picture']

class DailyCheckInForm(forms.ModelForm):
    class Meta:
        model = DailyCheckIn
        fields = ['skin_feel', 'new_blemishes', 'sleep_hours', 'hydration', 
                 'sun_exposure', 'stress_level', 'used_skincare']
        widgets = {
            'skin_feel': forms.RadioSelect,
            'new_blemishes': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'sleep_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '24'}),
            'hydration': forms.RadioSelect,
            'sun_exposure': forms.RadioSelect,
            'stress_level': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'used_skincare': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }
        labels = {
            'skin_feel': 'How does your skin feel today?',
            'new_blemishes': 'Did you notice any new blemishes or redness?',
            'sleep_hours': 'How many hours did you sleep last night?',
            'hydration': 'Did you drink enough water today?',
            'sun_exposure': 'Did you spend time in the sun today?',
            'stress_level': 'How stressed do you feel? (1 = least stressed, 5 = most stressed)',
            'used_skincare': 'Did you use any skincare products today?'
        }