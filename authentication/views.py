from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import LoginForm
from authentication.forms import RegisterForm


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'authentication/login.html', {'login_form': LoginForm()})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('all_products')

        return render(request, 'authentication/login.html', {'login_form': login_form})


class RegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'authentication/register.html', {'user_form': RegisterForm()})

    @staticmethod
    def post(request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('all_products')

        return render(request, 'authentication/register.html', {'user_form': user_form})


def logout_user(request):
    logout(request)
    return redirect('all_products')
