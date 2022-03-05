from .models import *


def user_status(request):
    status = request.session.get('user-role', None)
    return status


def user_info(request):
    email = request.session.get("email", None)
    us = None
    if email is not None:
        us = User.objects.get(email=email)
    return us



