from SongManager.models import Song, Tag, Composer, SongFile, FileType
from django.contrib import admin

admin.site.register(Song)
admin.site.register(Tag)
admin.site.register(Composer)
admin.site.register(SongFile)
admin.site.register(FileType)
