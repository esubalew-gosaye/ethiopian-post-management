from django.shortcuts import redirect
from account.inc import user_info, user_status
from django.contrib import messages


def login_first(view_func):
    def wrapper(request, *args, **kwargs):
        if user_info(request) is None:
            messages.error(request, "Please Login First To Access the page!")
            return redirect('account:login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Sorry, This Page is restricted to admin only!")
            return redirect('account:login')
    return wrapper


def user_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) == 'costumer':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Sorry, This Page is restricted to customer only!")
            return redirect('account:login')
    return wrapper


def postman_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) == 'postman':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Sorry, This Page is restricted to postman only!")
            return redirect('account:login')
    return wrapper


def manager_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) == 'manager':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Sorry, This Page is restricted to manager only!")
            return redirect('account:login')
    return wrapper


def counter_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) == 'counter':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Sorry, This Page is restricted to manager only!")
            return redirect('account:login')
    return wrapper

def your_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_status(request) is None:
            messages.error(request, "Sorry, Please login to access pages.")
            return redirect('account:login')
        else:
            flag = user_status(request)
            if flag == 'costumer':
                flag = 'user'
            return redirect(f"post:{flag}-dashboard")
            # return view_func(request, *args, **kwargs)
    return wrapper

