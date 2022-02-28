from .models import *


def user_info(request):
    status = request.session.get('user-role', None)
    email = request.session.get("email", None)

    us = User.objects.get(email=email)
    return us



