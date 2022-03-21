from symbol import try_stmt

from django.shortcuts import render, redirect
from .forms import *
from .inc import user_status, user_info
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from .models import User
from django.core.mail import EmailMessage


def login(request):
    fg = 'admin'
    rvk = request.GET.get("revoke")

    if request.method == "POST":
        if request.POST.get('email_field') is not None:
            em = request.POST.get('email')
            if Revoke.objects.filter(user__email=em).exists():
                messages.error(request, "Already password revoke is requested check your email.")
                qd = QueryDict("", mutable=True)
                qd.update({"revoke": "code", "email": em})
                return redirect(reverse('account:login') + f'?{qd.urlencode()}')
            else:
                try:
                    em_ = User.objects.get(email=em)
                    sd = Revoke(user=em_)
                    sd.save()
                    qd = QueryDict("", mutable=True)
                    qd.update({"revoke": "code", "email": em})
                    messages.success(request, "We have sent a message to your email.")
                    return redirect(reverse('account:login') + f'?{qd.urlencode()}')
                except:
                    messages.error(request, "Your email doesn't Exist in our database.")
        elif request.POST.get('code') is not None:
            em = request.GET.get('email')
            cd = request.POST.get('codechar')
            try:
                rv = Revoke.objects.get(user__email=em)
                if cd == rv.code:
                    messages.success(request, "Good Job please update your password.")
                    qd = QueryDict("", mutable=True)
                    qd.update({"revoke": "password", "id": rv.user.id})
                    email = EmailMessage("Hello,", f'Here is your code: {rv.code}', to=[em])
                    email.send()
                    rv.delete()
                    return redirect(reverse('account:login') + f'?{qd.urlencode()}')
                else:
                    messages.error(request, "The Code you have entered isn't correct.")
            except:
                messages.error(request, "Your email doesn't Exist in our database.")
        elif request.POST.get('login') is not None:
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
                elif user.is_manager:
                    flag = "manager"
                else:
                    flag = "costumer"
                request.session["user-role"] = flag
                request.session["email"] = user.email
                if flag == 'costumer': flag = 'user'
                messages.success(request, "Successfully logged in to system. welcome!")
                return redirect(f'post:{flag}-dashboard')
            else:
                messages.warning(request, "User doesn't exist!, with this credentials.")
    context = {
        'id': request.GET.get("id"),
        'role': fg,
        'revoke': rvk,
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
                elif role == "manager":
                    gs.is_manager = True
                else:
                    gs.is_costumer = True
                gs.save()
                messages.success(request, "User is successfully registered!")
                if role == 'customer':
                    messages.info(request, "Please login to proceed.")
                    return redirect("account:login")
                flag = user_status(request)
                if flag == 'costumer': flag = 'user'
                return redirect(f"post:{flag}-dashboard")
            else:
                messages.warning(request, "User Email is already taken.")
                return redirect(reverse('account:register', args=[role]))
    if role == 'customer':
        return render(request, "post/register.html", {"rf_form": rf})
    else:
        qd_ = QueryDict("", mutable=True)
        qd_.update({"pages": "new_client", 'new_user_role': role})
        flag = user_status(request)
        if flag == 'costumer': flag = 'user'
        return HttpResponseRedirect(reverse(f'post:{flag}-dashboard') + f'?{qd_.urlencode()}')


def update_account(request):
    id = request.GET.get('id')
    us_ = None
    if id is None:
        us_ = user_info(request)
    else:
        us_ = User.objects.get(id=id)
    if request.method == "POST":
        rs = RegisterForm(request.POST, instance=us_)
        if rs.is_valid():
            rs.save()
            messages.success(request, "Account is successfully updated!")
        else:
            messages.error(request, "Account is not updated!")
    flag = user_status(request)
    if flag == 'costumer': flag = 'user'
    return HttpResponseRedirect(reverse(f'post:{flag}-dashboard'))


def forgot_password(request):
    itm = request.GET.get('revoke')
    qd = QueryDict("", mutable=True)
    value = "true"
    if itm == 'true':
        value = "email"
    elif itm == "email":
        value = "code"
    qd.update({"revoke": value})
    return redirect(reverse('account:login') + f'?{qd.urlencode()}')


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
    if flag == 'costumer':
        flag = 'user'
    return redirect(reverse(f'post:{flag}-dashboard') + f'?{qd.urlencode()}')


def update_password_forgot(request, pk):
    qd = QueryDict("", mutable=True)
    if request.method == "POST":
        np = request.POST.get('new_password')
        rnp = request.POST.get('renew_password')
        if np != rnp:
            messages.warning(request, "Two password aren't match..")
            qd.update({'revoke': 'password', "id": pk})
        else:
            User.objects.filter(id=pk).update(password=np)
            messages.success(request, "Your password are successfully updated!")
    return redirect(reverse(f'account:login') + f'?{qd.urlencode()}')


def delete_user(request, pk):
    try:
        us = User.objects.get(id=pk)
        us.delete()
        messages.success(request, "User successfully deleted!")
    except:
        messages.error(request, "User doesn't exist!")
    return redirect(f'post:{user_status(request)}-dashboard')


def logout(request):
    request.session.pop("user-role", 0)
    request.session.pop("email", 0)
    return redirect('account:login')
