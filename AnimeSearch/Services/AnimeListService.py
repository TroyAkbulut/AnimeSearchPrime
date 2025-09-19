from ..models import AnimeListEntry, Folder, User
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