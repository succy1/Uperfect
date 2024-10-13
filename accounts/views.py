from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .quiz import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def skin_quiz(request):
    return render(request, 'skin-quiz.html', {'questions': SKIN_QUIZ})

@login_required
def profile(request):
    return render(request, 'profile.html')
