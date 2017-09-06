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
        print settings.JAVA_DIR
        #os.environ["CLASSPATH"] = os.environ["CLASSPATH"] + ":" + settings.JAVA_DIR if os.environ.has_key("CLASSPATH") else settings.JAVA_DIR
        #print os.environ["CLASSPATH"]
        #print ["java", "-cp", path.join(settings.JAVA_DIR, 'py4j0.9.jar')+":"+path.join(settings.JAVA_DIR, "/*"),settings.JAVA_DIR,"jchinte.py4j.POIEntryPoint"]
        #if not Event_PlannerConfig.gateway_on:
            #subprocess.Popen(["java", "-cp", path.join(settings.JAVA_DIR, 'py4j0.9.jar')+":"+path.join(settings.JAVA_DIR, "/*")+":"+settings.JAVA_DIR,"jchinte.py4j.POIEntryPoint"])
            #Event_PlannerConfig.gateway_on = True
        os.environ["LD_LIBRARY_PATH"] = "/home/jchinte/lib"
