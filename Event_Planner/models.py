from __future__ import unicode_literals
import os
from django.db import models
from django.core.files import File
from django.dispatch.dispatcher import receiver
from SongManager.models import Song, SongFile
from model_utils.managers import InheritanceManager
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import renderers
from music_planner0 import settings
import subprocess
#from SongManager.models import SongSegment
#from inheritance import ParentModel, ChildManager

# Create your models here.
class Event(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, blank=True)
    is_template = models.BooleanField(default=False)
    pptx = models.FileField(upload_to="songs/protected", null=True)
    

    def create_pptx(self):
        if self.has_ppt():
            songs = SongSegment.objects.filter(event=self.id).order_by("order")
            #TODO: segment_queryset = Segment.objects.select_subclasses().order_by('order')
            #get powerpoints related to songs
            blankFilename = "../black.pptx"
            pptFilenames = []
            for s in songs:
                if s.song:
                    files = SongFile.objects.filter(song=s.song.id, filetypes__type='Powerpoint')
                    for f in files:
                        newPath = f.file.name
                        _,file_extension = os.path.splitext(newPath)
                        if file_extension=='.pptx':
                            pptFilenames.append(os.path.basename(f.file.name))
                            pptFilenames.append(blankFilename)
            if len(pptFilenames)==0:
                return
            else:
                command =  ['./bin/pptMerge3', '-i'] + pptFilenames + ['-o', '../../../tmp/'+self.get_pptx_name()] 
                output = subprocess.run(command)
                fn = os.path.join(settings.BASE_DIR,'../../tmp/',self.get_pptx_name())
                f = open(fn, 'rb')
                django_file = File(f)
                self.pptx.save(self.get_pptx_name(), django_file, True)

    def get_pptx_name(self):
        return self.title+'.pptx'
    
    def invalidate_pptx(self):
        self.pptx.delete()
        print("Post invalidate: ", self.id, self.pptx if self.pptx else "none")


    def has_ppt(self):

        songs = SongSegment.objects.filter(event=self.id).order_by("order")
        for s in songs:
            if s.song:
                if SongFile.objects.filter(song=s.song.id, filetypes__type='Powerpoint'):
                    return True
        return False
    def copy_event(self, other__id):
        segments = Segment.objects.select_subclasses().filter(event=other__id)
        for segment in segments:
            segment.pk=None
            segment.id=None
            if str(segment.title) == 'Announcements':
                announcement = Song(title = "Announcements" + str(self.id), first_line = 'Announcements for ' + self.title)
                announcement.save()
                segment.song = announcement
            segment.event = self
            segment.save()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail_view', args=[str(self.pk)])#, [str(self.id)])
    
    class Meta:
        permissions = (
            ("can_create_template", "Can create an event template"),
        )
  
class Segment(models.Model):
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    event = models.ForeignKey(Event, related_name="segments", on_delete=models.CASCADE)
    
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
    song = models.ForeignKey(Song, on_delete=models.SET_NULL,blank=True, null=True)
    def getFiles(self):
        return SongFile.objects.filter(song__pk=self.song.id)
    files = property(getFiles)
   
class Role(models.Model):
    name = models.CharField(max_length=80)
    
    def __str__(self):
        return self.name
#    participants = models.ManyToManyField(User, through='Activity')
    #participants = models.ManyToManyField('Participant', through='Activity')
    

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    roles = models.ManyToManyField(Role, through='Activity')
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    segment_event = models.ForeignKey(Segment, on_delete=models.CASCADE)
    send_reminder = models.BooleanField()
    
@receiver(models.signals.post_save, sender=SongSegment)
def invalidate_event_pptx(sender, instance, *args, **kwargs):
    """ invalidates pptx on `post_save` """
    e = Event.objects.get(id=instance.event.id)
    e.invalidate_pptx()
    e = Event.objects.get(id=instance.event.id)
    #instance.event.invalidate_pptx()

import pytz
from datetime import datetime
def utc_to_local(dt):
    local = pytz.timezone('US/Pacific')
    localtime = dt.astimezone(local)
    naive = datetime(localtime.year, localtime.month, localtime.day, localtime.hour, localtime.minute)
    return pytz.utc.localize(naive)

def local_to_utc(dt):
    local = pytz.timezone('US/Pacific')
    naive = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=None)
    local_dt = local.localize(naive,is_dst=False)
    return local_dt
"""
events = Event.objects.all()
for event in events:
    d1 = event.date
    d2 = utc_to_local(event.date)
    d3 = local_to_utc(d2)
    print(event,":",d1,"->",d2,"->",d3) 

"""
