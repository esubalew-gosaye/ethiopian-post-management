from django.urls import include, path
from .views import *

app_name = "post"
urlpatterns = [
    path("", index, name="index-view"),
    path("test/", test, name="test-page"),
    path("admin/", admin_dashboard, name="admin-dashboard"),
    path("user/", user_dashboard, name="user-dashboard"),
    path("counter/", counter_dashboard, name="counter-dashboard"),
    path("postman/", postman_dashboard, name="postman-dashboard"),
    path("seen/<str:pk>/", all_to_seen, name="all-or-one-to-seen")
]
