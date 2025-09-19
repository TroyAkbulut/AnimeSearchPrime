import requests
import json
from types import SimpleNamespace
from ..UnmanagedModels.AnimeSearchResult import AnimeSearchResult
from ..UnmanagedModels.AnimeDetails import AnimeDetails

# TODO: Convert this to JS so it can run client side
# Currently all requests come from the server IP, meaning rate limiting will occur quickly
# Running JS on the browser will distribute the traffic across many IPs

# https://docs.api.jikan.moe/
class JinkanAPIService:
    baseURL = "https://api.jikan.moe/v4/"

    # TODO: replace these 2 with enums
    allowedTypes = ("tv", "movie", "ova", "special", "ona", "music", "cm", "pv", "tv_special")
    allowedStatuses = ("airing", "complete", "upcoming")

    @staticmethod
    def __CastSearchDataToAnimeSearchResult(dataList: list[SimpleNamespace]) -> list[AnimeSearchResult]:
        searchResults: list[AnimeSearchResult] = []

        for animeData in dataList:
            searchResult = AnimeSearchResult()

            searchResult.malID = animeData.mal_id
            searchResult.malURL = animeData.url
            searchResult.imageURL = animeData.images.jpg.image_url
            if animeData.title_english:
                searchResult.englishTitle = animeData.title_english
            else:
                searchResult.englishTitle = animeData.title
            searchResult.type = animeData.type

            if animeData.episodes:
                searchResult.episodes = animeData.episodes
            else:
                searchResult.episodes = 0
            searchResult.status = animeData.status
            searchResult.score = animeData.score
            searchResult.year = animeData.year

            searchResults.append(searchResult)

        return searchResults

    @staticmethod
    def __CastAnimeDataToAnimeDetail(animeData: SimpleNamespace) -> AnimeDetails:
        animeDetails = AnimeDetails()

        animeDetails.malID = animeData.mal_id
        animeDetails.malURL = animeData.url
        animeDetails.imageURL = animeData.images.jpg.image_url

        if animeData.title_english:
            animeDetails.mainTitle = animeData.title_english
        else:
            animeDetails.mainTitle = animeData.title

        if animeData.episodes:
            animeDetails.episodes = animeData.episodes
        else:
            animeDetails.episodes = 0

        animeDetails.titles = list()
        for title in animeData.titles:
            animeDetails.titles.append(title.title)

        animeDetails.type = animeData.type

        if animeData.title_english:
           animeDetails.englishTitle = animeData.title_english
        else:
            animeDetails.englishTitle = animeData.title

        animeDetails.status = animeData.status

        # date is formatted as yyyy-mm-ddThh:MM:ss+00:00
        # we only care for the date so we only take the first 10 characters
        animeDetails.startDate = getattr(animeData.aired, 'from')[:10]
        if animeData.aired.to:
            animeDetails.endDate = animeData.aired.to[:10]
        else:
            animeDetails.endDate = None

        animeDetails.score = animeData.score

        if animeData.scored_by:
            animeDetails.scoredBy = f'{animeData.scored_by:,}'
        else:
            animeDetails.scoredBy = '0'

        animeDetails.synopsis = animeData.synopsis
        animeDetails.background = animeData.background

        animeDetails.studios = list()
        for studio in animeData.studios:
            animeDetails.studios.append(studio.name)

        animeDetails.genres = list()
        for genre in animeData.genres:
            animeDetails.genres.append(genre.name)
        for genre in animeData.explicit_genres:
            animeDetails.genres.append(genre.name)
        for genre in animeData.themes:
            animeDetails.genres.append(genre.name)
        for genre in animeData.demographics:
            animeDetails.genres.append(genre.name)

        animeDetails.SetDisplayAttributes()

        return animeDetails

    @staticmethod
    def __MakeGetRequest(requestURL: str, queryParameters: dict[str, object] = dict()) -> list[SimpleNamespace]:
        response = requests.get(requestURL, queryParameters) # type: ignore
        jsonData = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
        return jsonData.data

    def GetAnimeSearch(self, page: int = -1, q: str = "", animeType: str = "", status: str = ""):
        # TODO: Add an enum for genres so that they can also be searched

        apiURL = self.baseURL + "anime"
        queryParameters: dict[str, object] = dict()

        if page >= 0:
            queryParameters["page"] = page

        if q != "":
            queryParameters["q"] = q

        if animeType in self.allowedTypes:
            queryParameters["type"] = animeType

        if status in self.allowedStatuses:
            queryParameters["status"] = status

        data = self.__MakeGetRequest(apiURL, queryParameters)

        searchResults = self.__CastSearchDataToAnimeSearchResult(data)
        return searchResults

    def GetAnimeByID(self, malID: int):
        apiURL = self.baseURL + f"anime/{malID}"
        data = self.__MakeGetRequest(apiURL)
        return self.__CastAnimeDataToAnimeDetail(data) # type: ignore
