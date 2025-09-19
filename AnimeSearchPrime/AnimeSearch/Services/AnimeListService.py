from ..models import AnimeListEntry, Folder, User
from ..UnmanagedModels.AnimeFolder import AnimeFolder
from django.db import transaction

class AnimeListService:
    def FindAnimeForUserByID(self, malID: int, userID: int|None) -> tuple[bool, AnimeListEntry|None]:
        animeListEntry = AnimeListEntry.objects.filter(malID=malID, user=userID)
        if animeListEntry:
            return True, animeListEntry[0]
        
        return False, None
    
    def GetFoldersForUser(self, userID: int|None) -> list[Folder]:
        folders = Folder.objects.filter(user=userID)
        folders = list(folders)
        return folders
    
    def CreateFolder(self, userID: int|None, folderName: str):
        user = User.objects.get(pk=userID)
        folder = Folder.objects.create(user=user, folderName=folderName)
        folder.save()
        
    def DeleteFolder(self, folderID: int):
        folders = list(Folder.objects.filter(pk=folderID))
        if not folders:
            return
        folder = folders[0]
        
        animeInFolder = AnimeListEntry.objects.filter(folder=folder)
        with transaction.atomic():
            for entry in animeInFolder:
                entry.delete()
        
        folders[0].delete()
        
    def RenameFolder(self, folderID: int, folderName: str):
        folder = Folder.objects.get(pk=folderID)
        folder.folderName = folderName
        folder.save()
        
    def AddAnime(self, folderID: int, malID: int, imageURL: str, mainTitle: str, userID: int|None):
        folder = Folder.objects.get(pk=folderID)
        user = User.objects.get(pk=userID)
        
        existingEntry = list(AnimeListEntry.objects.filter(malID=malID, user=user))
        if existingEntry:
            existingEntry = existingEntry[0]
            existingEntry.folder = folder
            existingEntry.save()
        
        else:
            animeEntry = AnimeListEntry.objects.create(user=user, folder=folder, malID=malID, imageURL=imageURL, mainTitle=mainTitle)
            animeEntry.save()
            
    def RemoveAnime(self, malID: int, userID: int|None):
        user = User.objects.get(pk=userID)
        existingEntry = AnimeListEntry.objects.get(user=user, malID=malID)
        existingEntry.delete()
        
    def GetAnimeListForUser(self, userID: int|None) -> list[AnimeFolder]:
        user = User.objects.get(pk=userID)
        folders = list(Folder.objects.filter(user=user))
        animeList = list(AnimeListEntry.objects.filter(user=user))
        
        animeFolders: list[AnimeFolder] = list()
        for folder in folders:
            animeFolder = AnimeFolder()
            animeFolder.folder = folder
            animeFolder.animeListEntries = list()
            animeFolders.append(animeFolder)
            
        for entry in animeList:
            animeFolder = [folder for folder in animeFolders if folder.folder == entry.folder][0]
            animeFolder.animeListEntries.append(entry)
            
        return animeFolders