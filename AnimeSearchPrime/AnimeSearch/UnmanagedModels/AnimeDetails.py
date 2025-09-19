class AnimeDetails:
    malID: int
    malURL: str
    imageURL: str
    mainTitle: str
    englishTitle: str
    titles: list[str]
    type: str
    episodes: int
    status: str
    startDate: str
    endDate: str|None
    score: int
    scoredBy: str  # this is a string so that it can be displayed in a more readable way
    synopsis: str
    background: str
    studios: list[str]
    genres: list[str]

    displayTitles = str
    displayStudios = str
    displayGenres = str

    def SetDisplayAttributes(self):
        self.displayTitles = ""
        self.displayStudios = ""
        self.displayGenres = ""

        for title in self.titles:
            self.displayTitles += f"{title}, "
        for studio in self.studios:
            self.displayStudios += f"{studio}, "
        for genre in self.genres:
            self.displayGenres += f"{genre}, "

        self.displayTitles = self.displayTitles.strip(", ")
        self.displayStudios = self.displayStudios.strip(", ")
        self.displayGenres = self.displayGenres.strip(", ")