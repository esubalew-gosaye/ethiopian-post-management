from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from .inc import *
from django.contrib import messages


def logout(request):
    request.session.pop("user-role", 0)
    request.session.pop("email", 0)
    return redirect('account:login')


def index(request):
    context = {"nav": navbar_tool(request)}
    return render(request, 'main/index.html', context)


def register(request, role="customer"):
    print(dict(request.session))
    if request.method == "POST":
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            if not User.objects.filter(email=request.POST.get("email")).exists():
                gs = rf.save(commit=False)
                if role == "admin":
                    gs.is_admin = True
                elif role == "counter":
                    gs.is_counter = True
                elif role == "postman":
                    gs.is_postman = True
                else:
                    gs.is_costumer = True
                gs.save()
                if role == "costumer" and request.session.get("admin") is None:
                    messages.info(request, "Please login to proceed.")
                    return redirect("account:login")
                return redirect("account:index")
            else:
                messages.warning(request, "User Email is already taken.")
                return redirect(reverse('account:register', args=[role]))
    rf = RegisterForm()
    return render(request, 'main/register.html', {"form": rf, "nav": navbar_tool(request)})


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email, password=password).exists():
            user = User.objects.get(email=email, password=password)
            flag = ""
            if user.is_admin:
                flag = "admin"
            elif user.is_counter:
                flag = "counter"
            elif user.is_postman:
                flag = "postman"
            else:
                flag = "costumer"
            request.session["user-role"] = flag
            request.session["email"] = user.email
            if flag == "admin":
                return redirect('account:admin-dashboard')
            return render(request, 'main/index.html', {"nav": navbar_tool(request)})
        else:
            messages.warning(request, "User doesn't exist!, with this credentials.")
    return render(request, 'main/login.html', {"nav": navbar_tool(request)})


def admin(request):
    users = None
    role = request.GET.get("role")
    if role == "admin":
        users = User.objects.filter(is_admin=True)
    elif role == "postman":
        users = User.objects.filter(is_postman=True)
    elif role == "costumer":
        users = User.objects.filter(is_costumer=True)
    else:
        users = User.objects.all()
    return render(request, "main/admin.html", {"users": users, "nav": navbar_tool(request)})
