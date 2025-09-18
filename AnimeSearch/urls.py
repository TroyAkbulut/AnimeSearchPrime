from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("<int:animeID>/", views.detail, name="detail"),
    path("login/", views.login, name="login"),
    path("api/register/", views.register, name="register"),
    path("api/logout/", views.logout, name="logout"),
]