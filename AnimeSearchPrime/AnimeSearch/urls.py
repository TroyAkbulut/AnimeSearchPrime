from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("<int:animeID>/", views.detail, name="detail"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("user/folders/", views.manageFolders, name="manageFolders"),
    path("login/", views.login, name="login"),
    
    path("api/register/", views.register, name="register"),
    path("api/logout/", views.logout, name="logout"),
    path("api/folders/new/", views.createFolder, name="createFolder"),
    path("api/folders/delete/", views.deleteFolder, name="deleteFolder"),
    path("api/folders/edit/", views.editFolder, name="editFolder"),
    path("api/list/add/", views.addToList, name="addToList"),
    path("api/list/remove/<int:animeID>/", views.removeFromList, name="removeFromList")
]