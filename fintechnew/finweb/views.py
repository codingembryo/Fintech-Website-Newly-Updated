from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import get_service_categories
from .models import Category


# Create your views here.

def home(request):
     return render(request, 'finweb/home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error trying to login")
            return redirect('login')
    return render(request, 'finweb/login.html', {})
            
def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return render(request, 'finweb/logout.html')

def about(request):
    return render(request, 'finweb/about.html')

def security(request):
    return render(request, 'finweb/security.html')

def faq(request):
    return render(request, 'finweb/faq.html')

def support(request):
    return render(request, 'finweb/support.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully...!!!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form':form})


@login_required
def profile_dashboard(request):
    context={}
    categories_qs=Category.objects.all()
    if categories_qs.exists():
        context['categories']=categories_qs
    else:
        get_service_categories()
        categories_qs=Category.objects.all()
        context['categories']=categories_qs
    return render(request, "finweb/dashboard.html", context)



