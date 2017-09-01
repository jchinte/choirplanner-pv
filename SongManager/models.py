from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.encoding import smart_text
from subprocess import Popen
from os import path

# Create your models here.
class Composer(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    
    
    def __unicode__(self):
        return (smart_unicode(self.first_name) + smart_unicode(' ') + smart_unicode(self.last_name))
    
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return smart_unicode(self.tag_name)

            

class Song(models.Model):
    title = models.CharField(max_length=200)
    composers = models.ManyToManyField(Composer, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    first_line = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.title
    
    def getFiles(self):
        return SongFile.objects.filter(song=self.pk)
    files = property(getFiles)
    
    class Meta:
        ordering = ["title"]
        
    @models.permalink
    def get_absolute_url(self):
        return ('song_detail_view', [str(self.id)])
    
    @models.permalink
    def get_update_url(self):
        return ('song_update_view', [str(self.id)])
    
    @models.permalink
    def get_delete_url(self):
        return ('song_delete_view', [str(self.id)])
    def search_terms(self):
        s = str(self.title)
        composers = Composer.objects.filter(song__pk=self.pk)
        for c in composers:
            s+=" "+str(c)
        return s

class SongFile(models.Model):
    #filename = models.CharField(max_length=200)
    file = models.FileField(upload_to='songs')
    song = models.ForeignKey(Song)
    comments = models.CharField(max_length=300, blank=True)
    filetypes = models.ManyToManyField('FileType')
    
    def name(self):
#        print "Name is called"
        return self.__unicode__()
    def types(self):
        t = FileType.objects.filter(songfile__song__pk=self.pk)
        
        return self.filetypes.all()
    def _rawtypes(self):
        ts =self.types()
        d = []
        print "types list: "
        print ts
        for t in ts:
            d.append(t.__unicode__())
        print "returning filtered: "
        print d
        return d
    
    def __unicode__(self):
        s = (str(self.file.name)).split('/')
#        print "__unicode__"
#        print s
        return unicode(s[len(s)-1])
    
    def save(self):
        res = super(SongFile, self).save()
        filename = path.splitext(self.file.path)
        if filename[1]=='.pdf':
            callList = ("gs -q -dNOPAUSE -sDEVICE=jpeg -dBATCH -dPDFFitPage=true -dDEVICEWIDTHPOINTS=170 -dDEVICEHEIGHTPOINTS=220 -r300 -sOutputFile="+filename[0]+".jpeg "+self.file.path).split()
            print(callList)
            Popen(callList)
        return res

class FileType(models.Model):
    type = models.CharField(max_length=80)
    def __unicode__(self):
        return smart_text(self.type).strip('\t\n\r\\ ')
