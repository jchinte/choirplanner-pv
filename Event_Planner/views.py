# Create your views here.
from django.shortcuts import render
from urlparse import urlparse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from models import Event, Segment, SongSegment, Activity, Participant, Role
from django.db.models import Max
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import redirect
from formsfields import ParticipantForm, ActivityForm, EventForm
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.forms.models import modelformset_factory, modelform_factory,\
    ModelForm
from django.forms import HiddenInput
from django.utils.encoding import smart_unicode
from SongManager.views import JSONResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView, BaseCreateView,\
    BaseDeleteView
import json
from SongManager.formsfields import SearchForm
from django.template.context import RequestContext
from django.template import Context, loader
from Event_Planner.formsfields import EventTemplateForm,\
    TemplateChoiceForm, EventCreateForm, AjaxActivityForm
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseServerError, FileResponse
from datetime import datetime, timedelta
import django_mobile
from SongManager.models import SongFile
import music_planner0.settings as settings
import os.path
from py4j.java_gateway import JavaGateway, GatewayParameters
from subprocess import check_output


#class SongUploadView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):

class BaseEventListView(ListView):
    #queryset=Event.objects.filter(is_template=False)
    context_object_name="event_list"
    def get_context_data(self, **kwargs):
        context = super(BaseEventListView, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            context.update({
                            'base': 'base.html'
                            })
        else:
            context.update({
                            'base': 'base.html'
                            })
        context.update({
                        'templates': TemplateChoiceForm(),
                        'page_id':'EventList'
                        })
        return context

class TemplateListView(BaseEventListView):
    def get_context_data(self, **kwargs):
        context = super(TemplateListView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'TemplateList'
                        })
    def get_queryset(self):
        return Event.objects.filter(is_template=True)

    @method_decorator(permission_required('can_create_template'))
    def dispatch(self, *args, **kwargs):

        return super(TemplateListView, self).dispatch(*args, **kwargs)


class EventListView(BaseEventListView):
    def get_queryset(self):
        return Event.objects.filter(is_template=False).exclude(date__lt=datetime.now() - timedelta(hours=24))

class EventArchiveView(BaseEventListView):

    def get_context_data(self, **kwargs):
        context = super(EventArchiveView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'ArchiveList'
                        })
        return context
    def get_queryset(self):
        return Event.objects.filter(is_template=False)

class OrderUpdateView(JSONResponseMixin, BaseUpdateView):
    model=Event
    fields='__all__'
    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'ArchiveList'
                        })
        return context
    def render_to_response(self, context):
        print self.request

        #print "ajax!!"
        #HTTPRequest(self.request)
        #print self.request.raw_post_data
        #print "request:"
        data=json.loads(self.request.body)
        #data = simplejson.loads(self.request.raw_post_data)
        #print data['array']
    #            for item, value in self.request.POST.items():
    #                print item, value
    #                for v in value:
    #                    print v

        qs = Segment.objects.filter(event=self.object.pk)
        i=1;
        for s in data['array']:
            num = s.split('_')[1]
            qs.filter(pk=num).update(order=i)
            #print i
            i=i+1
        return JSONResponseMixin.render_to_response(self, {})

class EventUpdateView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):
    model=Event

    template_name_suffix = '_form'
    form_class = EventForm
    context_object_name = "event"
    segment_queryset = Segment.objects.select_subclasses().order_by('order')

    def get_success_url(self):
        return reverse('event_detail_view', args=[self.object.pk])

    def get_form_class(self):
        if hasattr(self, 'object') and self.object is not None:
            if self.object.is_template:
                return EventTemplateForm
            else:
                return EventForm
        return self.form_class

    def __init__(self, *args, **kwargs):
        super(EventUpdateView,self).__init__(*args, **kwargs)

    @method_decorator(permission_required('Event_Planner.change_event'))
    def dispatch(self, *args, **kwargs):

        return super(EventUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)

        form_list = []
        segment_list = list(self.segment_queryset.filter(event=self.object.pk))
        i=0
        for seg in segment_list:
            new_form_class = modelform_factory(seg.__class__, fields='__all__', widgets={'event':HiddenInput})
            new_form = new_form_class(instance=seg, prefix=(u'segment-'+smart_unicode(seg.pk)))

            form_list.append(new_form)

            i = i+1
        context.update({'formlist': form_list,
                        'page_id': 'EventUpdate'+str(self.object.pk)})
        form = SearchForm()
        context.update({'search_form': form,})
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.has_key('add_seg'):
            return redirect('segment_create_view', kwargs['pk'])
        if request.GET.has_key('add_songseg'):
            return redirect('songsegment_create_view', kwargs['pk'])
        return super(EventUpdateView, self).get(request, *args, **kwargs)

    def render_to_response(self, context):
        print django_mobile.get_flavour()
        if self.request.method=='GET':
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)
        elif self.request.is_ajax() or self.request.GET.has_key('xhr'):
            print "ajax"
            data=json.loads(self.request.body)


            qs = Segment.objects.filter(event=self.object.pk)
            i=1;
            for s in data['array']:
                num = s.split('_')[1]
                qs.filter(pk=num).update(order=i)
                #print i
                i=i+1
            return JSONResponseMixin.render_to_response(self, {})
        else:
            print "not ajax"
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)

class JSONEventUpdateView(EventUpdateView):
    pass


class EventDetailView(DetailView):
    model=Event
    #queryset=Event.objects.filter(is_template=False)
    context_object_name = "event"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        segments = Segment.objects.filter(event=self.object.pk).filter(visible=True).order_by('order')
        """
        print segments
        for seg in segments:
            if isinstance(seg, SongSegment):
                t = loader.get_template('SongManager/files.html')
                if seg.song:
                    c = Context({
                        'files': SongFile.objects.filter(song__pk=seg.song.id),
                        'song': seg.song
                    })
                    filedata = t.render(c)
                    seg.files = filedata
        """
        context.update({'segments': segments,
                        'page_id':'EventDetail'+str(self.object.pk)})
        return context
class EventDeleteView(DeleteView):
#    pass
    def get_context_data(self, **kwargs):
        context = super(EventDeleteView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'EventDelete'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('Event_Planner.delete_event'))
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)

    model = Event
    def get_success_url(self):
        return reverse('event_list_view')

class ActivityCreateView(CreateView):
    model=Activity
    form_class = ActivityForm
    def get_context_data(self, **kwargs):
        context = super(ActivityCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'ActivityCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_activity'))
    def dispatch(self, *args, **kwargs):
        return super(ActivityCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        if self.request.POST.has_key('segment_event'):
            return super(ActivityCreateView, self).get_initial()
        url = self.request.path
        #print url
        match = resolve(urlparse(url)[2])
        #print match.kwargs['pk']
        segment = Segment.objects.get(pk=match.kwargs['pk'])
        initial = {
                   'segment_event': segment,
                   }
        return initial

    def get_success_url(self):
        #print self.kwargs
        match = resolve(urlparse(self.request.path)[2])

        return reverse('event_update_view', args=[match.kwargs['event_id']])
    def render_to_response(self, context):
        context.update({'curr_url': self.request.path})
        return super(ActivityCreateView, self).render_to_response(context)

@cache_page (60*15)
def EventPowerpointView2(request, pk, filename):


    #print pk
    #get all items related to event
    songs = SongSegment.objects.filter(event=pk).order_by("order")
    #TODO: segment_queryset = Segment.objects.select_subclasses().order_by('order')
    #print songs

    #get powerpoints related to songs
    #blankFilename = os.path.join(settings.MEDIA_ROOT, "black.pptx")
    blankFilename = "../black.pptx"
    pptFilenames = []
    #pptFilenames.append(blankFilename)
    for s in songs:
        print s
        if s.song:
            files = SongFile.objects.filter(song=s.song.id, filetypes__type='Powerpoint')
            print str(s)+":"+ "all files: " + str(files)
            for f in files:
                print f.file.name

                print os.path.join(settings.MEDIA_ROOT, f.file.name)
                #newPath = os.path.join(settings.MEDIA_ROOT, f.file.name)
                newPath = f.file.name
                _,file_extension = os.path.splitext(newPath)
                print file_extension
                if file_extension=='.pptx':
                    #pptFilenames.append(os.path.join(settings.MEDIA_ROOT, f.file.name))
                    pptFilenames.append(os.path.basename(f.file.name))
                    pptFilenames.append(blankFilename)


    print pptFilenames
    if len(pptFilenames)==0:
        return HttpResponse("")
    else:
        #gateway = JavaGateway(gateway_parameters=GatewayParameters(address=settings.JAVA_GATEWAY_ADDRESS))
        #print gateway.help()
        #javaFilenames = gateway.new_array(gateway.jvm.java.lang.String, len(pptFilenames))
        #for i in range(len(pptFilenames)):
        #    javaFilenames[i] = pptFilenames[i]
        #    print pptFilenames[i] + "!!"
        #newFile = gateway.entry_point.mergePPTsToFile(javaFilenames)
        print "starting pptx"
        command =  ['/home/jchinte/bin/newpptMerge', os.path.join(settings.MEDIA_ROOT, 'songs/')] + pptFilenames
        print command
        output = check_output(command)
        print output
        ols = output.splitlines()
        newFile = "/home/jchinte/tmp/MergedPresentation.pptx"
        for l in ols:
            if l.startswith("target:"):
                newFile = l.split()[1]
        print "newfile " + newFile + " created"
        response = FileResponse(open(newFile, "rb"))
        #response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        if (filename==None or filename == "" ):
            filename = Event.objects.get(id=pk).title + '.pptx'
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        print response['Content-Disposition']
        response['content_type']='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        response['Content_Length'] = os.path.getsize(newFile)
        #response.write(newFile)

        return response
@cache_page (60*15)
def EventPowerpointView(request, pk):
    return EventPowerpointView2(request, pk, Event.objects.get(id=pk).title + '.pptx')

class AjaxActivityCreateView(JSONResponseMixin, BaseCreateView):
    model=Activity
    form_class = AjaxActivityForm
    template_name='Event_Planner/ajax_activity_form.html'
    activity_list_template_name='Event_Planner/new_activity_form.html'
    def get_context_data(self, **kwargs):
        context = super(AjaxActivityCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'AjaxActivityCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_activity'))
    def dispatch(self, request, *args, **kwargs):
        #print "dispatch reached"
        return super(AjaxActivityCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        #print self.request.POST
        if self.request.POST.has_key('segment_event'):
            return super(AjaxActivityCreateView, self).get_initial()
        url = self.request.path
        #print url
        match = resolve(urlparse(url)[2])
        #print match.kwargs['pk']
        segment = Segment.objects.get(pk=match.kwargs['pk'])
        initial = {
                   'segment_event': segment,
                   }
        return initial
    def post(self, request, *args, **kargs):
        self.object=None
        #print "post reached"
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            c = RequestContext(self.request, Context())
            #print c

            c.update({'segment': form.instance.segment_event})
            #print c
            t = loader.get_template(self.activity_list_template_name)
            #print t
            activities = t.render(c)
            #print activities
            return JSONResponseMixin.render_to_response(self, {'success':"Activity saved",
                                                               'activities': activities})
        else:
            print "invalid form"
            if form._errors.has_key('participant_name'):
                pass
                #print "no part name"
            else:
                pass
                #print "other error"
            #print "returning form invalid"
            return self.form_invalid(form)




    def render_to_response(self, context):
        #print"render"
        context.update({'curr_url': self.request.path})
        #print context
        c = RequestContext(self.request, context)
        t = loader.get_template(self.template_name)
        segdata = t.render(c)
        #ajax_dictionary.update({'html': segdata})
#        response = super(SingleObjectTemplateResponseMixin, self).render_to_response(context)
#        print response.content
        #print segdata
        con = Context()
        con.update({'data': segdata})
        return JSONResponseMixin.render_to_response(self, {'data':segdata})

class ActivityDeleteView(DeleteView):
#    pass
    model = Activity
    def get_context_data(self, **kwargs):
        context = super(ActivityDeleteView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'ActivityDelete'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('Event_Planner.delete_activity'))
    def dispatch(self, *args, **kwargs):
        return super(ActivityDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        match = resolve(urlparse(self.request.path)[2])
        return reverse('event_update_view', args=[match.kwargs['event_id']])
#    def get_context_data(self, **kwargs):
#        context = super(ActivityDeleteView, self).get_context_data(**kwargs)
#        context.update({'segment': self.request.path})
class ParticipantCreateView(CreateView):
    form_class = ParticipantForm
    template_name = "Event_Planner/generic_form.html"
    def get_context_data(self, **kwargs):
        context = super(ParticipantCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'ParticipantCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_partcipant'))
    def dispatch(self, *args, **kwargs):
        return super(ParticipantCreateView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context):
        if self.request.GET.has_key('back_url'):
            context.update({'back_url': self.request.GET['back_url']})
        return super(ParticipantCreateView, self).render_to_response(context)

    def get_success_url(self):
        if self.request.GET.has_key('back_url'):
            return self.request.GET['back_url']
        return reverse('event_list_view')

class RoleCreateView(CreateView):
    template_name = "Event_Planner/generic_form.html"
    model = Role
    def get_context_data(self, **kwargs):
        context = super(RoleCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'RoleCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_role'))
    def dispatch(self, *args, **kwargs):
        return super(RoleCreateView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context):
        if self.request.GET.has_key('back_url'):
            context.update({'back_url': self.request.GET['back_url']})
        return super(RoleCreateView, self).render_to_response(context)

    def get_success_url(self):
        if self.request.GET.has_key('back_url'):
            return self.request.GET['back_url']
        return reverse('event_list_view')


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'EventCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_event'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('can_create_template'):
            self.form_class=EventCreateForm
        return super(EventCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        print "success url: event_update_view " + str(self.object.pk)
        return reverse('event_update_view', args=[self.object.pk])
    def render_to_response(self, context):
        #print "createview render to response"
        #print context
        return super(EventCreateView, self).render_to_response(context)

class MassCreateView(EventCreateView):
    def get_context_data(self, **kwargs):
        context = super(MassCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'MassCreate'})
        return context
    def form_valid(self, form):
        response = super(MassCreateView, self).form_valid(form)
        SongSegment(order=1, title='Processional', event=self.object).save()
        SongSegment(order=2, title='Gloria', event=self.object).save()
        SongSegment(order=3, title='Responsorial Psalm', event=self.object).save()
        SongSegment(order=4, title='Gospel Acclamation', event=self.object).save()
        SongSegment(order=5, title='Preparation of the Gifts', event=self.object).save()
        SongSegment(order=6, title='Holy', event=self.object).save()
        SongSegment(order=7, title='Mystery of Faith', event=self.object).save()
        SongSegment(order=8, title='Great Amen', event=self.object).save()
        SongSegment(order=9, title='Lamb of God', event=self.object).save()
        SongSegment(order=10, title='Communion', event=self.object).save()
        SongSegment(order=11, title='Song of Praise', event=self.object).save()
        SongSegment(order=12, title='Recessional', event=self.object).save()
        #segment.save()
        return response

class TemplateCreateView(EventCreateView):
    form_class=EventForm

#    @method_decorator(permission_required('Event_Planner.can_create_template'))
#    def dispatch(self, *args, **kwargs):
#        return super(EventCreateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(TemplateCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'TemplateCreate'})
        return context

    def post(self, request, *args, **kwargs):
        print "POST"
        print self.request
        if self.request.GET.has_key('template'):
            self.template=self.request.GET['template']
        return super(TemplateCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(TemplateCreateView, self).form_valid(form)
        print "form is valid"
        print response
        if hasattr(self, 'template') and self.template is not None:
            print "has template " + str(self.template)
            segments = Segment.objects.select_subclasses().filter(event=self.template)
            for segment in segments:
                #print segment
                #print segment.pk
                segment.pk=None
                segment.id=None
                segment.event = self.object
                segment.save()
                #print "new ID:"
                #print segment.id
        return response



class SegmentCreateView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseCreateView):
    model = Segment
    template_name_suffix = '_form'
    title = None
    def get_context_data(self, **kwargs):
        context = super(SegmentCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SegmentCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_segment'))
    def dispatch(self, *args, **kwargs):
        return super(SegmentCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        if self.request.POST.has_key('event'):
            return super(SegmentCreateView, self).get_initial()
        if (self.request.META.has_key('HTTP_REFERER')):
            url = self.request.META['HTTP_REFERER']
        else:
            pass
        url = self.request.path
        print self.request.path

        match = resolve(urlparse(url)[2])
        print match
        event = Event.objects.get(pk=match.kwargs['event_id'])
        max_order = event.segment_set.aggregate(Max('order'))
        if max_order['order__max']:
            new_order = max_order['order__max'] + 1
        else:
            new_order = 1
        if self.title:
            title = self.title
        else:
            title = "segment"
        initial = {
                   'event': event,
                   'order': new_order,
                   'title': title,
                   }
        return initial

    def get_success_url(self):

            #print self.object.event.pk
            return reverse('event_update_view', args=[self.object.event.pk])
    def get_form_kwargs(self):
        kwargs = super(SegmentCreateView, self).get_form_kwargs()
        #print "segmentcreateview - "
        if self.object:
            kwargs.update({'prefix': (u'segment-'+smart_unicode(self.object.pk))})
        #print kwargs
        return kwargs
    def render_to_response(self, context):
        #print self.request
        if self.request.is_ajax() or self.request.GET.has_key('xhr'):
            ajax_dictionary = {}
            initial = self.get_initial()
            self.object = self.model(order=initial['order'], title=initial['title'], event=initial['event'])
            self.object.save()
            prefix=(u'segment-'+smart_unicode(self.object.pk))
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            c={
                      'form': form,
                      'event': initial['event']
                      }
            c = RequestContext(self.request, c)
            t = loader.get_template('Event_Planner/new_seg_form.html')
            print t
            segdata = t.render(c)
            ajax_dictionary.update({'html': segdata})
            return JSONResponseMixin.render_to_response(self, ajax_dictionary)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)




class SongSegmentCreateView(SegmentCreateView):
    model = SongSegment
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super(SongSegmentCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongSegmentCreate'})
        return context
    @method_decorator(permission_required('Event_Planner.add_songsegment'))
    def dispatch(self, *args, **kwargs):
        return super(SongSegmentCreateView, self).dispatch(*args, **kwargs)



class SegmentUpdateView(UpdateView):
    queryset = Segment.objects.select_subclasses()
    def get_context_data(self, **kwargs):
        context = super(SegmentUpdateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SegmentUpdate'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('Event_Planner.change_segment'))
    def dispatch(self, *args, **kwargs):
        return super(SegmentUpdateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SegmentUpdateView, self).get_form_kwargs()
        #print "segmentupdateview - "
        match = resolve(urlparse(self.request.path)[2])
        kwargs.update({'prefix': (u'segment-'+smart_unicode(match.kwargs['pk']))})
        #print kwargs
        return kwargs

    def get_success_url(self):
        #print self.object.event.pk
        return reverse('event_update_view', args=[self.object.event.pk])

class JSONSegmentUpdateView(JSONResponseMixin, BaseUpdateView):
    queryset = Segment.objects.select_subclasses()
    def get_object(self, queryset=None):
        ### this method must be called via post.
        ### this method should NEVER be called via get.
        print "get object!!!!!!!!!"
        self.object = super(JSONSegmentUpdateView, self).get_object(queryset)

        if isinstance(self.object, SongSegment):
            print "is song segment"
            pass
        elif self.object is not None:
            print "is reg segment"
            seg = self.object
            self.object = SongSegment()
            self.object.pk = seg.pk
            #self.object.delete()
            #self.object=None
        #print "end get object"
        return self.object
    @method_decorator(permission_required('Event_Planner.change_segment'))
    def dispatch(self, *args, **kwargs):
        print "dispatch called"
        return super(JSONSegmentUpdateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        print "get_form_class reached"
        new_form_class = modelform_factory(self.get_object().__class__, fields='__all__')
        return new_form_class


    def get_form_kwargs(self):
        kwargs = super(JSONSegmentUpdateView, self).get_form_kwargs()
        print "jsonsegmentupdateview - "
        match = resolve(urlparse(self.request.path)[2])
        kwargs.update({'prefix': (u'segment-'+smart_unicode(match.kwargs['pk']))})
        #print kwargs
        return kwargs
    def form_valid(self, form):
        # save form
        print "saving"
        #print form
        #result =  BaseUpdateView.form_valid(self, form)
        form.save()
        #print "saved"
        # return nothing
        return self.render_to_response({})
    #### TODO: present elegant form invalid response
    def form_invalid(self, form):
        print "form invalid"
        #print form
        return HttpResponseServerError("could not save form")
#        return BaseUpdateView.form_invalid(self, form)
#    def post(self, *args, **kargs):
#        print "IN POST"
#        self.object = self.get_object()
#        self.object.delete()
#        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
#        print "after super post"
#        return self.render_to_response({})
#    def get_success_url(self):
#        print self.object.event.pk
#        return reverse('event_update_view', args=[self.object.event.pk])

class SongSegmentUpdateView(SegmentUpdateView):
    queryset=Segment.objects.select_subclasses()
    model = SongSegment
    def get_context_data(self, **kwargs):
        context = super(SongSegmentUpdateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongSegmentUpdate'+str(self.object.pk)})
        return context
    def get_form_class(self):
        print "get_form_class reached!"
        new_form_class = modelform_factory(self.get_object().__class__, fields='__all__')
        return new_form_class
    def get_object(self, queryset=None):
        ### this method must be called via post.
        ### this method should NEVER be called via get.
        #print "get object!!!!!!!!!"
        self.object = super(SongSegmentUpdateView, self).get_object(queryset)

        if isinstance(self.object, SongSegment):
            pass
        elif self.object is not None:
            #print "is reg segment"
            seg = self.object
            self.object = SongSegment()
            self.object.pk = seg.pk
            #self.object.delete()
            #self.object=None
        #print "end get object"
        return self.object

class SegmentDeleteView(DeleteView):

    model = Segment
    def get_context_data(self, **kwargs):
        context = super(SegmentDeleteView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SegmentDelete'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('Event_Planner.delete_segment'))
    def dispatch(self, *args, **kwargs):

        return super(SegmentDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        match = resolve(urlparse(self.request.path)[2])
        return reverse('event_update_view', args=[match.kwargs['event_id']])

#################TODO: ADD PERMISSIONS DECORATORS TO JSON views


class JSONSegmentDeleteView(JSONResponseMixin, BaseDeleteView):
    model = Segment
    def post(self, *args, **kargs):
        #print "IN POST"
        self.object = self.get_object()
        self.object.delete()
        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
        #print "after super post"
        return self.render_to_response({})

class JSONActivityDeleteView(JSONResponseMixin, BaseDeleteView):
    model = Activity
    def post(self, *args, **kargs):
        #print "IN POST"
        self.object = self.get_object()
        self.object.delete()
        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
        #print "after super post"
        return self.render_to_response({})

# non-generic views


@login_required
def JSONRoleListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        roles = Role.objects.filter(name__icontains=term)
    else:
        roles = Role.objects.all()
    role_list = []
    for role in roles:
        role_list.append(smart_unicode(role))

    response = HttpResponse(json.dumps(role_list,  ensure_ascii=False))
    return response

@login_required
def JSONParticipantListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        participants = Participant.objects.filter(name__icontains=term)
    else:
        participants = Participant.objects.all()
    participant_list = []
    for participant in participants:
        participant_list.append(smart_unicode(participant))

    response = HttpResponse(json.dumps(participant_list,  ensure_ascii=False))
    return response
@login_required
def JSONPDFView(request, event_id):
    print request
    if request.method=='GET':
        songs = SongSegment.objects.filter(event=event_id).order_by("order")
        pdfSongs = []
        for s in songs:
            print s
            if s.song:
                songInfo = {}
                songInfo['title'] = s.song.title
                songInfo['files'] = []
                files = SongFile.objects.filter(song=s.song.id)
                print str(s)+":"+ "all files: " + str(files)
                for f in files:
                    print f.file.name

                    print os.path.join(settings.MEDIA_ROOT, f.file.name)
                    newPath = os.path.join(settings.MEDIA_ROOT, f.file.name)
                    file_root,file_extension = os.path.splitext(newPath)
                    print file_extension
                    if file_extension=='.pdf':
                        fileInfo = {}
                        fileInfo['id']=f.id
                        fileInfo['types'] = [type.__unicode__() for type in f.types()]
                        if len(fileInfo['types'])==0:
                            fileInfo['types'] = ['file']
                        if os.path.isfile(file_root+'.jpeg'):
                            fileInfo['thumbnail'] = settings.MEDIA_URL+os.path.splitext(f.file.name)[0] + '.jpeg'
                        songInfo['files'].append(fileInfo)
                        #pdfFilenames.append(os.path.join(settings.MEDIA_ROOT, f.file.name))
                        #pptFilenames.append(blankFilename)
                if songInfo['files']:
                    pdfSongs.append(songInfo)
        return HttpResponse(json.dumps(pdfSongs, ensure_ascii=False))
@login_required
def getSongs(event_id):
    songs = SongSegment.objects.filter(event=event_id).order_by("order")
    fs = []
    for s in songs:
        if s.song:
            files = SongFile.objects.filter(song=s.song.id)
            for f in files:
                newPath = os.path.join(settings.MEDIA_ROOT, f.file.name)
                _,file_extension = os.path.splitext(newPath)
                if file_extension=='.pdf':
                    fs.append(os.path.join(settings.MEDIA_ROOT, f.file.name))
    return fs

def RESTEventView(request):
    def get(request):
        pass
    def post(request):
        return HTTPResponse(status=405)
    def put(request):
        return HTTPResponse(status=405)
    def delete(request):
        return HTTPResponse(status=405)
    methods = {
        'GET': get,
        'POST': post,
        'PUT': put,
        'DELETE': delete
    }
    #dispatch
    return methods[request.method](request)

@login_required
def RawPDFView(request, event_id):
    if request.method=='GET':
        fs = [os.path.join(settings.MEDIA_ROOT, SongFile.objects.get(pk=i).file.name) for i in request.GET.getlist('fid[]')] if 'fid[]' in request.GET \
         else getSongs(event_id)
        print("qpdf --empty --decrypt --pages".split() + fs + "-- -".split())
        combinedFile = check_output("/home/jchinte/bin/qpdf --empty --decrypt --pages".split() + fs + "-- -".split())
        response = HttpResponse(str(combinedFile), content_type='application/pdf')
        filename = Event.objects.get(id=event_id).title + '.pdf'
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        print response['Content-Disposition']
        response['Content_Length'] = len(combinedFile)
        return response
        #return HttpResponse(json.dumps(pdfSongs, ensure_ascii=False))
