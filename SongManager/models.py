from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_text, python_2_unicode_compatible
from subprocess import Popen
from music_planner0 import settings
from os import path
import os
from django.dispatch import receiver

# Create your models here.
@python_2_unicode_compatible
class Composer(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return (smart_text(self.first_name) + smart_text(' ') + smart_text(self.last_name))
    
@python_2_unicode_compatible
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    
    def __str__(self):
        return smart_text(self.tag_name)

            

@python_2_unicode_compatible
class Song(models.Model):
    title = models.CharField(max_length=200)
    composers = models.ManyToManyField(Composer, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    first_line = models.CharField(max_length=500)
    
    def __str__(self):
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


@python_2_unicode_compatible
class SongFile(models.Model):
    #filename = models.CharField(max_length=200)
    file = models.FileField(upload_to='songs')
    song = models.ForeignKey(Song)
    comments = models.CharField(max_length=300, blank=True)
    filetypes = models.ManyToManyField('FileType')
    
    def name(self):
        return self.__str__()
    def types(self):
        t = FileType.objects.filter(songfile__song__pk=self.pk)
        
        return self.filetypes.all()
    def _rawtypes(self):
        ts =self.types()
        d = []
        for t in ts:
            d.append(t.__str__())
        return d
    
    def __str__(self):
        s = (str(self.file.name)).split('/')
        return unicode(s[len(s)-1])
    def __thumbnail(self):
        filename = path.splitext(self.file.path)
        if filename[1]=='.pdf':
            return path.join(settings.MEDIA_URL, 'songs/', path.basename(filename[0])+'.jpeg')
        else:
            return None
    thumbnail = property(__thumbnail)

    def save(self):
        res = super(SongFile, self).save()
        filename = path.splitext(self.file.path)
        if filename[1]=='.pdf':
            callList = ("gs -q -dNOPAUSE -sDEVICE=jpeg -dBATCH -dPDFFitPage=true -dDEVICEWIDTHPOINTS=170 -dDEVICEHEIGHTPOINTS=220 -r300 -sOutputFile="+filename[0]+".jpeg "+self.file.path).split()
            Popen(callList)
        return res



@python_2_unicode_compatible
class FileType(models.Model):
    type = models.CharField(max_length=80)
    def __str__(self):
        return smart_text(self.type).strip('\t\n\r\\ ')


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=SongFile)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.file:
        _delete_file(instance.file.path)
