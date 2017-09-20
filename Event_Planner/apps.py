from django.apps import AppConfig
import subprocess
from os import path
from music_planner0 import settings
import os

class Event_PlannerConfig(AppConfig):
    name = 'Event_Planner'
    verbose_name = "Event Planner"
    gateway_on = False
    def ready(self):
        super(Event_PlannerConfig, self).ready()
        os.environ["LD_LIBRARY_PATH"] = "/home/jchinte/lib"
