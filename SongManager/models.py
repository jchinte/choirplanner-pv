from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_str
from subprocess import Popen
from music_planner0 import settings
from os import path
import os
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
import mimetypes
from rest_framework.authtoken.models import Token

# Create your models here.
class Composer(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return (smart_str(self.first_name) + smart_str(' ') + smart_str(self.last_name))
    
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    
    def __str__(self):
        return smart_str(self.tag_name)

class Song(models.Model):
    title = models.CharField(max_length=200)
    composers = models.ManyToManyField(Composer, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    first_line = models.CharField(max_length=500)
    
    def __str__(self):
        return smart_str(self.title)
    
    def getFiles(self):
        return SongFile.objects.filter(song=self.pk)
    #files = property(getFiles)
    
    class Meta:
        ordering = ["title"]
        
    def get_absolute_url(self):
        return reverse('song_detail_view', args=[str(self.id)])
    
    def get_update_url(self):
        return reverse('song_update_view', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('song_delete_view', args=[str(self.id)])

    def search_terms(self):
        return str(self.title) + " " + " ".join(str(c) for c in Composer.objects.filter(song__pk=self.pk))

class SongFile(models.Model):
    #filename = models.CharField(max_length=200)
    file = models.FileField(upload_to='songs')
    song = models.ForeignKey(Song, related_name="files", on_delete=models.CASCADE)
    comments = models.CharField(max_length=300, blank=True)
    filetypes = models.ManyToManyField('FileType')
    
    def name(self):
        return str(self)
    def types(self):
        #t = FileType.objects.filter(songfile__song__pk=self.pk)        
        return self.filetypes.all()
    def _rawtypes(self):
        return [str(t) for t in self.types()]
    
    def __str__(self):
        s = (str(self.file.name)).split('/')
        return smart_str(s[len(s)-1])
    def __thumbnail(self):
        filename = path.splitext(self.file.path)
        if filename[1]=='.pdf':
            return path.join(settings.MEDIA_URL, 'songs/', path.basename(filename[0])+'.jpeg')
        else:
            return None
    thumbnail = property(__thumbnail)

    def save(self, *args, **kwargs):
        res = super(SongFile, self).save(*args, **kwargs)
        filename = path.splitext(self.file.path)
        if filename[1]=='.pdf':
            callList = ("gs -q -dNOPAUSE -sDEVICE=jpeg -dBATCH -dPDFFitPage=true -dDEVICEWIDTHPOINTS=170 -dDEVICEHEIGHTPOINTS=220 -r300 -sOutputFile="+filename[0]+".jpeg "+self.file.path).split()
            Popen(callList).wait(5)
        return res

class FileType(models.Model):
    type = models.CharField(max_length=80)
    def __str__(self):
        return smart_str(self.type).strip('\t\n\r\\ ')


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

def invalidate_pptx(instance):
    from Event_Planner.models import SongSegment
    segments = SongSegment.objects.filter(song=instance.song)
    events = set(map(lambda seg:seg.event, segments))
    for e in events:
        e.invalidate_pptx()

@receiver(models.signals.post_delete, sender=SongFile)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.file:
        if mimetypes.guess_type(instance.file.path)[0]=='application/vnd.openxmlformats-officedocument.presentationml.presentation':
            invalidate_pptx(instance)
        _delete_file(instance.file.path)

@receiver(models.signals.post_save, sender=SongFile)
def invalidate_event_pptx(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.file:
        if mimetypes.guess_type(instance.file.path)[0]=='application/vnd.openxmlformats-officedocument.presentationml.presentation':
            invalidate_pptx(instance)


@receiver(models.signals.post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
