from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return redirect('all_products')
