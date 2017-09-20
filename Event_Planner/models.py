from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from SongManager.models import Song, SongFile
from model_utils.managers import InheritanceManager
from django.contrib.auth.models import User
#from SongManager.models import SongSegment
#from inheritance import ParentModel, ChildManager

# Create your models here.
@python_2_unicode_compatible
class Event(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, blank=True)
    is_template = models.BooleanField(default=False)
    
    def get_pptx_name(self):
        return self.title+'.pptx'
    
    def has_ppt(self):

        songs = SongSegment.objects.filter(event=self.id).order_by("order")
        for s in songs:
            if s.song:
                if SongFile.objects.filter(song=s.song.id, filetypes__type='Powerpoint'):
                    return True
        return False

    def __str__(self):
        return self.title

     
    @models.permalink
    def get_absolute_url(self):
        return ('event_detail_view', [str(self.pk)])#, [str(self.id)])
    
    class Meta:
        permissions = (
            ("can_create_template", "Can create an event template"),
        )

@python_2_unicode_compatible    
class Segment(models.Model):
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    event = models.ForeignKey(Event)
    
    objects = InheritanceManager()
    visible = models.BooleanField(default=True)
#    objects = models.Manager()
#    children = ChildManager()
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["order"]
 #   def get_parent_model(self):
 #       return Segment
    
class LinkedSegment(Segment):
    link = models.URLField()

class SongSegment(Segment):
    song = models.ForeignKey(Song, blank=True, null=True)
    def getFiles(self):
        return SongFile.objects.filter(song__pk=self.song.id)
    files = property(getFiles)

@python_2_unicode_compatible    
class Role(models.Model):
    name = models.CharField(max_length=80)
    
    def __str__(self):
        return self.name
#    participants = models.ManyToManyField(User, through='Activity')
    #participants = models.ManyToManyField('Participant', through='Activity')
    
@python_2_unicode_compatible
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    roles = models.ManyToManyField(Role, through='Activity')
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    role = models.ForeignKey(Role)
    participant = models.ForeignKey(Participant)
    segment_event = models.ForeignKey(Segment)
    send_reminder = models.BooleanField()
    
    
