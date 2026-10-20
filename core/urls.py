from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots, name="robots"),
    path("cookie-uri/", views.cookies, name="cookies"),
]
