from django.shortcuts import render
from django.urls import reverse
from account.inc import user_info
from django.http import HttpResponseRedirect
from account.models import User
from .models import *
from .forms import *
from django.contrib import messages


def test(request):
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
    }
    return render(request, "main/test.html", context)


def index(request):
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
    }
    return render(request, "post/index.html", context)


def admin_dashboard(request):
    page = request.GET.get('pages')
    if page is not None and page[:3] == "reg":
        return HttpResponseRedirect(reverse('account:register', args=[page[4:]]))
    users = User.objects.all()
    if page is not None and page[:5] == 'user_':
        if page[5:] == "admin":
            users = users.filter(is_admin=True)
        elif page[5:] == 'counter':
            users = users.filter(is_counter=True)
        elif page[5:] == 'postman':
            users = users.filter(is_postman=True)
        else:
            users = users.filter(is_costumer=True)
    if request.method == "POST":
        if request.POST.get('mail_cost') is not None:
            ob = Config.objects.all()
            if len(list(ob)) > 0:
                up = ob[0]
                up.distance = request.POST.get('length')
                up.cost = request.POST.get('cost')
                up.save()
            else:
                ob = Config(distance=request.POST.get('length'), cost=request.POST.get('cost'))
                ob.save()
        elif request.POST.get('photo_upload') is not None:
            fr = ImageUploadForm(request.POST, request.FILES)
            if fr.is_valid():
                f = fr.cleaned_data
                d = Carousel(title=f.get('title'), caption=f.get('caption'), photo=f.get('image'))
                d.save()
                messages.debug(request, "Your photo successfully uploaded")
    context = {
        'page': page,
        'users': users,
        'user': user_info(request)
    }
    return render(request, 'post/admin-page.html', context)


def counter_dashboard(request):
    page = request.GET.get('pages')
    context = {
        'page': page,
    }
    return render(request, 'post/counter-page.html', context)


def user_dashboard(request):
    page = request.GET.get('pages')
    context = {
        'page': page,
    }
    return render(request, 'post/user-page.html', context)


def postman_dashboard(request):
    page = request.GET.get('pages')
    context = {
        'page': page,
    }
    return render(request, 'post/postman-page.html', context)