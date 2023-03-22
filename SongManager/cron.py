from SongManager.models import Song, Composer

def cleanComposers():
    cs = Composer.objects.all()
    emptys = [c for c in cs if len(Song.objects.filter(composers__in=[c]))==0]
    for e in emptys:
        e.delete()

