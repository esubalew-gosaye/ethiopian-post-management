from .models import *


def navbar_tool(request):
    status = request.session.get('user-role', None)
    email = request.session.get("email", None)
    name = None
    if email is not None:
        name = User.objects.get(email=email).first_name
    return {"status": status, "email": email, "name": name}



