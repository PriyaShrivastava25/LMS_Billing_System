from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, "signup.html")
