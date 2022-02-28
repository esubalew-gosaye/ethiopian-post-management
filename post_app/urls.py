from django.urls import include, path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = "post"

urlpatterns = [
    path("", index, name="index-view"),
    path("test/", test, name="test-page"),
    path("admin/", admin_dashboard, name="admin-dashboard"),
    path("user/", user_dashboard, name="user-dashboard"),
    path("counter/", counter_dashboard, name="counter-dashboard"),
    path("postman/", postman_dashboard, name="postman-dashboard"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
