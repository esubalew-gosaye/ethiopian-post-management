from symbol import try_stmt

from django.shortcuts import render, redirect
from .forms import *
from .inc import user_status
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from .models import User


def login(request):
    fg = 'admin'
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
            fg = flag
            request.session["email"] = user.email
            if flag == 'costumer': flag = 'user'
            messages.success(request, "Successfully logged in to system. welcome!")
            return redirect(f'post:{flag}-dashboard')
        else:
            messages.warning(request, "User doesn't exist!, with this credentials.")
    context = {
        'role': fg
    }
    return render(request, "post/login.html", context)


def register(request, role):
    rf = RegisterForm()
    if request.method == 'POST':
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
                messages.success(request, "User is successfully registered!")
                if role == 'customer':
                    messages.info(request, "Please login to proceed.")
                    return redirect("account:login")
                return redirect("post:admin-dashboard")
            else:
                messages.warning(request, "User Email is already taken.")
                return redirect(reverse('account:register', args=[role]))
    if role == 'customer':
        return render(request, "post/register.html", {"rf_form": rf})
    else:
        return render(request, 'post/admin-page.html', {"rf_form": rf})


def update_password(request, pk):
    if request.method == "POST":
        cp = request.POST.get('current_password')
        np = request.POST.get('new_password')
        rnp = request.POST.get('renew_password')
        if np != rnp:
            messages.warning(request, "Your new and reenter password aren't much.")
        else:
            us = User.objects.get(id=pk)
            if us.password != cp:
                messages.warning(request, "Your new and old password aren't much.")
            else:
                us.password = np
                us.save()
                messages.success(request, "Your password are successfully updated!")
    qd = QueryDict("", mutable=True)
    qd.update({'pages': 'profile'})
    flag = user_status(request)
    if flag == 'costumer': flag = 'user'
    return redirect(reverse(f'post:{flag}-dashboard')+f'?{qd.urlencode()}')


def delete_user(request, pk):
    try:
        us = User.objects.get(id=pk)
        us.delete()
        messages.success(request, "User successfully deleted!")
    except:
        messages.error(request, "User doesn't exist!")

    return redirect('post:admin-dashboard')

def logout(request):
    request.session.pop("user-role", 0)
    request.session.pop("email", 0)
    return redirect('account:login')
