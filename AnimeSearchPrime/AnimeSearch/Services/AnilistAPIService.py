import requests
import json
import re
from types import SimpleNamespace
from ..UnmanagedModels.AnimeSearchResult import AnimeSearchResult
from ..UnmanagedModels.AnimeDetails import AnimeDetails

# TODO: Convert this to JS so it can run client side
# Currently all requests come from the server IP, meaning rate limiting will occur quickly
# Running JS on the browser will distribute the traffic across many IPs

# https://docs.anilist.co/guide/graphql/queries/media
# https://studio.apollographql.com/sandbox/explorer

class AnilistAPIService:
    baseURL = "https://graphql.anilist.co"

    # TODO: replace these 2 with enums
    allowedTypes = ("tv", "movie", "ova", "special", "ona", "music", "cm", "pv", "tv_special")
    allowedStatuses = ("airing", "complete", "upcoming")
    
    htmlTagRegex = re.compile(r'<[^>]+>')

    @staticmethod
    def __CastSearchDataToAnimeSearchResult(dataList: list[SimpleNamespace]) -> list[AnimeSearchResult]:
        searchResults: list[AnimeSearchResult] = []

        for animeData in dataList:
            searchResult = AnimeSearchResult()

            searchResult.malID = animeData.idMal
            searchResult.imageURL = animeData.coverImage.large
            if animeData.title.english:
                searchResult.englishTitle = animeData.title.english
            else:
                searchResult.englishTitle = animeData.title.romaji

            if animeData.episodes:
                searchResult.episodes = animeData.episodes
            else:
                searchResult.episodes = 0
            searchResult.status = animeData.status
            
            if animeData.averageScore:
                searchResult.score = animeData.averageScore/10
            else:
                searchResult.score = 0
                
            searchResult.year = animeData.seasonYear

            searchResults.append(searchResult)

        return searchResults

    @staticmethod
    def __CastAnimeDataToAnimeDetail(animeData: SimpleNamespace) -> AnimeDetails:
        animeDetails = AnimeDetails()

        animeDetails.malID = animeData.idMal
        animeDetails.imageURL = animeData.coverImage.extraLarge

        if animeData.title.english:
            animeDetails.englishTitle = animeData.title.english
        else:
            animeDetails.englishTitle = animeData.title.romaji
            
        animeDetails.mainTitle = animeDetails.englishTitle
            
        animeDetails.titles = list()
        if animeDetails.englishTitle != animeData.title.romaji:
            animeDetails.titles.append(animeData.title.romaji)
        animeDetails.titles.append(animeData.title.native)
        animeDetails.titles.extend(animeData.synonyms)

        if animeData.episodes:
            animeDetails.episodes = animeData.episodes
        else:
            animeDetails.episodes = 0

        animeDetails.status = animeData.status

        animeDetails.startDate = f"{animeData.startDate.year}-{animeData.startDate.month:02d}-{animeData.startDate.day:02d}"
        if animeData.endDate.year and animeData.endDate.month and animeData.endDate.day:
            animeDetails.endDate = f"{animeData.endDate.year}-{animeData.endDate.month:02d}-{animeData.endDate.day:02d}"
        else:
            animeDetails.endDate = None

        if animeData.averageScore:
            animeDetails.score = animeData.averageScore/10
        else:
            animeDetails.score = 0

        scoredBy = 0
        for scoredCount in animeData.stats.scoreDistribution:
            scoredBy += scoredCount.amount
        animeDetails.scoredBy = f'{scoredBy:,}'

        animeDetails.synopsis = animeData.description
        animeDetails.background = ""

        animeDetails.studios = list()
        for studio in animeData.studios.nodes:
            animeDetails.studios.append(studio.name)

        animeDetails.genres = animeData.genres

        animeDetails.SetDisplayAttributes()
        return animeDetails

    @staticmethod
    def __MakePostRequest(requestURL: str, operation: str, variables: dict[str, object] = dict()) -> SimpleNamespace:
        response = requests.post(requestURL, json={"query": operation, "variables": variables}) # type: ignore
        jsonData = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
        return jsonData.data

    def GetAnimeSearch(self, search: str = ""):
        # TODO: Add an enum for genres so that they can also be searched

        queryOperation = """
query($search: String, $perPage: Int, $type: MediaType = ANIME, $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC])  {
	Page(perPage: $perPage){
		media(search: $search, type: $type, sort: $sort)  {
			id
			title {
				romaji
				english
				native
			}
			idMal
			coverImage {
				large
			}
			episodes
			status
			averageScore
			seasonYear
		}
	}
}
        """
        variables = {
            "search": search,
            "perPage": 25
        }
        data = self.__MakePostRequest(self.baseURL, queryOperation, variables)
        searchResults = self.__CastSearchDataToAnimeSearchResult(data.Page.media)
        return searchResults
    
    def GetDefaultAnimeSearch(self):
        queryOperation = """
query($perPage: Int, $type: MediaType = ANIME, $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC])  {
    Page(perPage: $perPage){
        media(type: $type, sort: $sort)  {
            id
            title {
                romaji
                english
                native
            }
            idMal
            coverImage {
                large
            }
            episodes
            status
            averageScore
            seasonYear
        }
    }
}
        """
        
        variables: dict[str, object] = {
            "perPage": 25
        }
        data = self.__MakePostRequest(self.baseURL, queryOperation, variables)
        searchResults = self.__CastSearchDataToAnimeSearchResult(data.Page.media)
        return searchResults

    def GetAnimeByID(self, malID: int):
        queryOperation = """
query Query($idMal: Int) {
    Media(idMal: $idMal) {
        idMal
        coverImage {
            extraLarge
        }
        title {
            english
            romaji
            native
        }
        episodes
        synonyms
        status
        startDate {
            day
            month
            year
        }
        endDate {
            day
            month
            year
        }
        averageScore
        stats {
            scoreDistribution {
                amount
            }
        }
        description
        studios {
            nodes {
                name
            }
        }
        genres
    }
}
        """
        
        data = self.__MakePostRequest(self.baseURL, queryOperation, {"idMal": malID})
        return self.__CastAnimeDataToAnimeDetail(data.Media)
