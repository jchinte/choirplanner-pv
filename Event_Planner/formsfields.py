from __future__ import unicode_literals
from Event_Planner.models import Participant, Activity, Event
from django.forms import ModelForm, HiddenInput, SplitDateTimeWidget, \
            SplitDateTimeField, CharField, DateInput, TimeInput
from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from Event_Planner.models import Role
from django import forms
#from django.forms.widgets import HiddenInput


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'email')

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ('role', 'participant', 'segment_event', 'send_reminder')
        widgets = {
                   'segment_event' : HiddenInput
                   }
class EventCreateForm(ModelForm):
    date = SplitDateTimeField(input_time_formats=[
                                                 '%I:%M %p',
                                                 '%I:%M%p',
                                          #       '%H:%M:%S',
                                                '%H:%M',
                                                 ])
    class Meta:
        model = Event
        fields=('date', 'title', 'is_template',)
        #widgets = {'date': SplitDateTimeWidget}



class SplitDateTimeWidget2(SplitDateTimeWidget):
    def __init__(self, attrs1=None, attrs2=None, date_format=None, time_format=None):
        super(SplitDateTimeWidget2, self).__init__(None, date_format, time_format)
        widgets = (DateInput(attrs=attrs1, format=date_format),
                   TimeInput(attrs=attrs2, format=time_format))
class EventForm(ModelForm): # alsjdsljh
    date = SplitDateTimeField(widget=SplitDateTimeWidget(date_format="%Y-%m-%d",
                                                          time_format='%I:%M %p'),input_time_formats=[
                                               '%I:%M %p',
                                                 '%I:%M%p',
    #                                             '%H:%M:%S',
                                               '%H:%M',
                                                ])
    class Meta:
        model = Event 
        exclude=('is_template','')

        
class EventTemplateForm(ModelForm):
    class Meta:
        model = Event
        fields=('title',)

    
class TemplateChoiceForm(Form):
    
    template = ModelChoiceField(queryset=Event.objects.filter(is_template=True).order_by('-date'),\
                                empty_label=None)
#    search = CharField(max_length=200)
#    options = ChoiceField(SEARCH_CHOICES)

class AjaxActivityForm(ModelForm):
    role_name = CharField()
    participant_name = CharField()
    
    def clean_participant_name(self):
        data = self.cleaned_data['participant_name']
        try:
            self.participant = Participant.objects.get(name=data)
            self.cleaned_data['participant']=self.participant
        except:
            raise forms.ValidationError("Participant does not exist")
        return data
    def clean_role_name(self):
        data = self.cleaned_data['role_name']
        self.role, created = Role.objects.get_or_create(name=data)
        self.cleaned_data['role']=self.role
        return data
    def save(self):
        self.instance.role = self.role
        self.instance.participant = self.participant
        return self.instance.save()
      
    
    class Meta:
        model=Activity
        exclude=('role', 'participant')
        widgets = {'segment_event': HiddenInput}
