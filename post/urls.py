from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', include("post_app.urls")),
    path('account/', include("account.urls")),
]
