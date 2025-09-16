from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

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

def login(request: WSGIRequest):
    if request.method == "GET":
        template = loader.get_template("login.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
