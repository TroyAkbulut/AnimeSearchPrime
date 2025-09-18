from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as authLogin
from django.contrib.auth import logout as authLogout
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("logger")

from .UnmanagedModels import AnimeSearchResult
from .Services.JinkanAPIService import JinkanAPIService
#from .Services.AnimeListService import AnimeListService

jinkanAPIService = JinkanAPIService()
#animeListService = AnimeListService()

def index(request: WSGIRequest):
    animeSearchResults = jinkanAPIService.GetAnimeSearch()
    template = loader.get_template("index.html")
    context = {
        "animeSearchResults": animeSearchResults,
        "searchQuery": ""
    }

    return HttpResponse(template.render(context, request))

def search(request: WSGIRequest):
    searchQuery = request.GET["searchQuery"]

    animeSearchResults = jinkanAPIService.GetAnimeSearch(q=searchQuery)
    template = loader.get_template("index.html")
    context = {
        "animeSearchResults": animeSearchResults,
        "searchQuery": searchQuery
    }

    return HttpResponse(template.render(context, request))

def detail(request, animeID):
    #exists, animeEntry = animeListService.FindAnimeByID(animeID)
    activeFolder = None
    animeDetail = jinkanAPIService.GetAnimeByID(animeID)
    #if exists:
    #    activeFolder = animeEntry.folder
        

    #folders = animeListService.GetFolderNames()

    template = loader.get_template("detail.html")
    context = {
        "folderNames": ["Good", "Great", "Masterpiece"], #folders,
        "activeFolder": activeFolder,
        "animeDetail": animeDetail
    }

    return HttpResponse(template.render(context, request))

def login(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "GET":
        template = loader.get_template("login.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
    elif request.method == "POST":
        username = request.POST["loginUsername"]
        password = request.POST["loginPassword"]
        logger.warning(username)
        logger.warning(password)
        user = authenticate(username=username, password=password)
        if not user:
            template = loader.get_template("login.html")
            context = {
                "registerErrors": [],
                "loginErrors": ["Username or password is incorrect"]
            }
            return HttpResponse(template.render(context, request))
        
        else:
            authLogin(request, user)
            return redirect("index")
    
def register(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        username = request.POST["registerUsername"]
        email = request.POST["registerEmail"]
        password = request.POST["registerPassword"]
        
        if User.objects.filter(username__iexact=username).exists():
            template = loader.get_template("login.html")
            context = {
                "registerErrors": ["Username already exists"],
                "loginErrors": []
            }
            return HttpResponse(template.render(context, request))
        
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        authLogin(request, user)
        
        return redirect("index")
    
@login_required(login_url="login/")
def logout(request: WSGIRequest):
    authLogout(request)
    return redirect("index")