from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    folderID = models.AutoField(db_column='FolderID', primary_key=True)
    folderName = models.CharField(db_column='FolderName', max_length=255, blank=False, null=False)
    
    class Meta:
        db_table = "Folder"
        managed = True
        
        
class AnimeListEntry(models.Model):
    animeListEntryID = models.AutoField(db_column='AnimeListEntryID', primary_key=True)
    user = models.ForeignKey(User, models.PROTECT, db_column='User', blank=False, null=False)
    folder = models.ForeignKey(Folder, models.PROTECT, db_column='Folder', blank=False, null=False)
    malID = models.IntegerField(db_column="MalID", blank=False, null=False)
    ImageURL = models.CharField(db_column='ImageURL', max_length=255, blank=False, null=False)
    mainTitle = models.CharField(db_column='MainTitle', max_length=255, blank=False, null=False)
    
    class Meta:
        db_table = "AnimeListEntry"
        managed = True