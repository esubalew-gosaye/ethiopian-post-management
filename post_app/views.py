from django.shortcuts import render, redirect
from django.urls import reverse
from account.inc import user_info, user_status
from django.http import HttpResponse, HttpResponseRedirect
from account.models import User
from .models import *
from datetime import datetime, timedelta
from .forms import *
from account.forms import RegisterForm
from django.contrib import messages
from django.http import QueryDict

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


def test(request):
    qdict = QueryDict("", mutable=True)
    qdict.update({'pages': 'profile'})
    dd = qdict.urlencode()
    daily = Post.objects.filter(date_send__year='2022', date_send__month='3', date_send__day='1',)
    # HttpResponseRedirect(reverse('post:admin-dashboard')+f"?{dd}")
    if request.method == 'POST':
        s = request.POST.get('date').split('-')
        daily = Post.objects.filter(date_send__year=s[0], date_send__month=s[1], date_send__day=s[2], )

        posts = Post.objects.all()

        # weekly
        now = datetime.today()
        week_ago = now - timedelta(days=7)
        weekly = Post.objects.filter(date_send__range=[week_ago, now])

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        response["Content-Transfer-Encoding"] = 'binary'
        html_string = render_to_string('post/report.html', {'posts': posts, 'total': 0})
        html = HTML(string=html_string)

        rs = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(rs)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response
    context = {
        'time': 'weekly',
        'user': user_status(request),
        'post': Post.objects.all(),
    }
    return render(request, 'main/test.html', context)


def index(request):
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
    }
    return render(request, "post/index.html", context)


def admin_dashboard(request):
    page = request.GET.get('pages')
    user_inf = user_info(request)

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
    u_form = RegisterForm(instance=user_inf)
    if page == "update_user":
        _i = User.objects.get(id=request.GET.get('id'))
        u_form = RegisterForm(instance=_i)

    if request.method == "POST":
        if request.POST.get('mail_cost') is not None:
            ob = Config.objects.all()
            if len(list(ob)) > 0:
                up = ob[0]
                up.weight = request.POST.get('weight')
                up.cost = request.POST.get('cost')
                up.save()
                messages.success(request, "Mail cost updated!")
            else:
                ob = Config(distance=request.POST.get('length'), cost=request.POST.get('cost'))
                ob.save()
                messages.success(request, "Mail cost saved!")

        elif request.POST.get('photo_upload') is not None:
            fr = ImageUploadForm(request.POST, request.FILES)
            if fr.is_valid():
                f = fr.cleaned_data
                d = Carousel(title=f.get('title'), caption=f.get('caption'), photo=f.get('image'))
                d.save()
                messages.success(request, "Your photo successfully uploaded")
        elif request.POST.get('update') is not None:
            rs = RegisterForm(request.POST, instance=user_inf)
            if rs.is_valid():
                rs.save()
                messages.success(request, "Account is successfully updated!")
            else:
                messages.error(request, "Account is not updated!")
        elif request.POST.get('update_s_user') is not None:
            hidden_id = request.GET.get('id')
            try:
                rs = RegisterForm(request.POST, instance=User.objects.get(id=hidden_id))
                if rs.is_valid():
                    rs.save()
                    messages.success(request, "User profile is successfully updated!")
                    return redirect('post:admin-dashboard')
                else:
                    messages.error(request, "User profile is not updated!")
            except:
                messages.error(request, "User id isn't fetched correctly!")
    context = {
        'page': page,
        'users': users,
        'user': user_inf,
        'role': user_status(request),
        'notify': Post.objects.filter(receiver=user_inf, seen=False),
        'update_form': u_form,
        'feedbacks': Feedback.objects.all(),
        'post_list': [
            Post.objects.filter(sender=user_inf),
            Post.objects.filter(receiver=user_inf)
        ],
    }
    return render(request, 'post/admin-page.html', context)


def counter_dashboard(request):
    page = request.GET.get('pages')
    user_inf = user_info(request)
    conf = Config.objects.last()

    if request.method == "POST":
        if request.POST.get('register_post') is not None:
            sd = PostForm(request.POST)
            sd.save()
            messages.success(request, "New Post is registered!")
        elif request.POST.get('assign_postman') is not None:
            post_id = request.POST.get('post_id')
            postman_id = request.POST.get('postman_assigned')
            us = Post.objects.get(id=post_id)
            us.postman = User.objects.get(id=postman_id)
            us.save()
            messages.success(request, "Postman is successfully assigned!")
        elif request.POST.get('update_location') is not None:
            post_item = request.POST.getlist('post_select')
            loc = request.POST.get('location')
            for pk in post_item:
                _u = Post.objects.get(id=pk)
                _u.post_location = loc
                _u.save()
            messages.success(request, "Post location is updated!")
    if page == 'generate_report':
        if request.GET.get('time') == "daily":
            if request.method == 'POST':
                s = request.POST.get('date').split('-')
                daily = Post.objects.filter(date_send__year=s[0], date_send__month=s[1], date_send__day=s[2])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                response["Content-Transfer-Encoding"] = 'binary'
                html_string = render_to_string('post/report.html', {'posts': daily})
                html = HTML(string=html_string)
                rs = html.write_pdf()
                with tempfile.NamedTemporaryFile(delete=True) as output:
                    output.write(rs)
                    output.flush()
                    output.seek(0)
                    response.write(output.read())
                return response
        elif request.GET.get('time') == "weekly":
            now = datetime.today()
            week_ago = now - timedelta(days=7)
            weekly = Post.objects.filter(date_send__range=[week_ago, now])
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            response["Content-Transfer-Encoding"] = 'binary'
            html_string = render_to_string('post/report.html', {'posts': weekly})
            html = HTML(string=html_string)

            rs = html.write_pdf()
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(rs)
                output.flush()
                output.seek(0)
                response.write(output.read())
            return response

    context = {
        'page': page,
        'user': user_inf,
        'cost': conf,
        'role': user_status(request),
        'notify': Post.objects.filter(receiver=user_inf, seen=False),
        'update_form': RegisterForm(instance=user_inf),
        'post_form': PostForm(),
        'posts': Post.objects.all(),
        'postman': User.objects.filter(is_postman=True),
        'post_list': [
            Post.objects.filter(sender=user_inf),
            Post.objects.filter(receiver=user_inf)
        ],
    }
    return render(request, 'post/counter-page.html', context)


def user_dashboard(request):
    page = request.GET.get('pages')
    user_inf = user_info(request)
    tr = None
    if request.method == "POST":
        if request.POST.get('feedback') is not None:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            fd = Feedback(name=name, email=email, subject=subject, body=message)
            fd.save()
            messages.success(request, "Thank you, we value your feedback.")
        elif request.POST.get('track') is not None:
            tr = Post.objects.get(track_id=request.POST.get('track_id'))

    context = {
        'page': page,
        'track': tr,
        'user': user_inf,
        'notify': Post.objects.filter(receiver=user_inf, seen=False),
        'role': user_status(request),
        'update_form': RegisterForm(instance=user_inf),
        'post_list': [
            Post.objects.filter(sender=user_inf),
            Post.objects.filter(receiver=user_inf)
        ],
    }
    return render(request, 'post/user-page.html', context)


def postman_dashboard(request):
    page = request.GET.get('pages')
    user_inf = user_info(request)
    if request.method == "POST":
        if request.POST.get('update_location') is not None:
            post = request.POST.getlist('post_select')
            loc = request.POST.get('location')
            for pk in post:
                u = Post.objects.get(id=pk)
                u.post_location = loc
                u.save()
            messages.success(request, "Post location is updated!")
    context = {
        'page': page,
        'user': user_inf,
        'role': user_status(request),
        'notify': Post.objects.filter(receiver=user_inf, seen=False),
        'update_form': RegisterForm(instance=user_inf),
        'post_list': [
            Post.objects.filter(sender=user_inf),
            Post.objects.filter(receiver=user_inf),
            Post.objects.filter(postman=user_inf)
        ],
    }
    return render(request, 'post/postman-page.html', context)


def all_to_seen(request, pk):
    us = user_info(request)
    if pk == 'none':
        itm = Post.objects.filter(receiver=us, seen=False)
    else:
        itm = Post.objects.filter(id=pk, receiver=us, seen=False)
    for i in itm:
        i.seen = True
        i.save()
    usr = user_status(request)
    if usr == "customer": usr = "user"
    return redirect(f'post:{usr}-dashboard')
