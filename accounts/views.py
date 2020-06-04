from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from .forms import CustomForm, CustomLogin

# Create your views here.
def signup_views(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect("Home.html")
    else:
        form = CustomForm()
    return render(request,'accounts/Signup.html',{'form': form })
def login_views(request):
    if request.user.is_authenticated:
        return redirect('/Home/')
        
    if request.method == "POST":
        form = CustomLogin(data=request.POST)
        if form.is_valid():
            #login
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect("/Home/")
    else:
        form = CustomLogin()
    return render(request,'accounts/Login.html', {'form': form })    
def logout_views(request):
    if request.method == 'GET':
        logout(request)
    return redirect("/Home/")
