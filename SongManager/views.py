# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect
from django.template import Context, loader
#from django.template.context import RequestContext
from models import Song, SongFile
from formsfields import SongFileForm, SongForm, SearchForm
from django import http
from django.http import Http404, HttpResponse
from django.views.generic import DeleteView, DetailView, UpdateView, ListView, CreateView
from django.views.generic.edit import SingleObjectTemplateResponseMixin, BaseUpdateView
#from django.utils import simplejson as json
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core import serializers
from SongManager.models import Composer, FileType, Tag
from django.utils.encoding import smart_unicode
from django.core.cache import cache

#mixins

class SearchQueryMixin(object):
    def search(self, searchTerms, opts, objects):
        cacheString = "search"+str(searchTerms)+str(opts)+str(objects)
        print "cacheString: "+cacheString
        qset = cache.get(cacheString)
        if qset is not None:
            print "cache hit"
            return qset
        print "cache miss"
        query = Q()
        for search_term in searchTerms:
            if opts=='B':
                q = (Q(title__icontains=search_term))
            elif opts=='C':
                q = (Q(tags__tag_name__icontains=search_term))
            elif opts=='D':
                q = (Q(composers__first_name__icontains=search_term)
                     | Q(composers__last_name__icontains=search_term))
            elif opts=='E':
                q = (Q(first_line__icontains=search_term))
            else:
                q = (Q(title__icontains=search_term) 
                     | Q(composers__first_name__icontains=search_term) 
                     | Q(composers__last_name__icontains=search_term) 
                     | Q(tags__tag_name__icontains=search_term) 
                     | Q(first_line__icontains=search_term))
            query = (query & q)
        qset = objects.filter(query).distinct()
        cache.set(cacheString, qset, 120)
        return qset

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        r = self.get_json_response(self.convert_context_to_json(context))
        return r
    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)
       

#class-based generic views

class SongDetailView(DetailView):
    context_object_name = "song"
    model = Song
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SongDetailView, self).dispatch(*args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            context.update({
                            'base': 'base.html'
                            })
        else:
            context.update({
                            'base': 'base.html'
                            })
        context.update({
                        'page_id':'SongDetail'+str(self.object.id)
                        })
        #print "context: "
        #print context
        t = loader.get_template('SongManager/files.html')
        c = Context({
            'files': SongFile.objects.filter(song__pk=self.object.id),
            'youtube': True
        })
        c.update({'song':self.object})
        filedata = t.render(c)
        context.update({'files': filedata })
        
        if (self.request.META.has_key('HTTP_REFERER')):
            context.update({'back_url':self.request.META['HTTP_REFERER']})
        
        return context

class SongUploadView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):
    context_object_name = "song"
    model = Song
    template_name_suffix = '_form'
    fields='__all__'
    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongUpload'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('SongManager.add_songfile'))
    def dispatch(self, *args, **kwargs):
        return super(SongUploadView, self).dispatch(*args, **kwargs)
       
    def render_to_response(self, context):
        #print "upload reached"
        if not self.request.POST:
            #print "not post"
            raise Http404
        #print "post reached"
        xhr = self.request.GET.has_key('xhr')
        #if xhr:
        #    print "true"
        #else:
        #    print "false"
        form = SongFileForm(self.request.POST, self.request.FILES)
        context.update({
                     'files': SongFile.objects.filter(song__pk=self.object.id),
                     'delete': 'True',
                     'song_pk': self.kwargs['pk'],
                        })
        if form.is_valid():
            form.save()
            
            if xhr:
                #print "is ajax?"
                #print self.request
                #print self.request.is_ajax()
                #print "xhr branch"
                t = loader.get_template('SongManager/files.html')
                c = Context({'delete': 'True', 'song_pk': self.kwargs['pk'],})
                c.update({'files': SongFile.objects.filter(song__pk=self.object.id),})
                filedata = t.render(c)
                response_dict = {
                                 'filedata': filedata,
                                 'delete': 'True',
                                 'song_pk': self.kwargs['pk'],
                                  'debug' : 'debug',
                                 }
                return JSONResponseMixin.render_to_response(self, response_dict)
            else:
                #print "non-xhr branch"
                return redirect('song_update_view', pk=self.kwargs['pk'])
        else:
            #print "form is invalid"
            return redirect('song_update_view', pk=self.kwargs['pk'])
    
class SongUpdateView(UpdateView):
    context_object_name = "song"
    model = Song
    form_class=SongForm
    template_name_suffix = '_form'
    @method_decorator(permission_required('SongManager.change_song'))
    def dispatch(self, *args, **kwargs):
        return super(SongUpdateView, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('song_list_view')

    def get_context_data(self, **kwargs):
        context = super(SongUpdateView, self).get_context_data(**kwargs)
        
        songfile_upload_form = SongFileForm(initial={'song': self.object.id})
        compList = []
        for c in Composer.objects.all():
            compList.append(c.__unicode__())
        fileTypeList = []
        for t in FileType.objects.all():
            fileTypeList.append(t.__unicode__())
        tagList = []
        for n in Tag.objects.all():
            tagList.append(n.__unicode__())
        context.update({
                        'file_form': songfile_upload_form,
                        'files': SongFile.objects.filter(song__pk=self.object.id),
                        'delete': 'True',
                        'edit': 'True',
                        'song_pk': self.kwargs['pk'],
                        'page_id': "SongUpdate"+str(self.object.id),
                        'composers': compList,
                        'file_types': fileTypeList,
                        'tags': tagList
                    })
        
        
        return context



class SongListView(JSONResponseMixin, ListView, SearchQueryMixin):

    model=Song
    context_object_name="song_list"                                
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongList'})
        return context
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SongListView, self).dispatch(*args, **kwargs)    

    def get_Page_dictionary(self, page_object):
        #print "page object"
        page_dict = {
                     'has_next': page_object.has_next(),
                     'has_previous': page_object.has_previous(),
                     'has_other_pages': page_object.has_other_pages(),
                     'start_index': page_object.start_index(),
                     'end_index': page_object.end_index(),
                     'number': page_object.number,
                     'num_pages': page_object.paginator.num_pages,
                     'page_size': self.paginate_by,
                     }
        if page_object.has_next():
            page_dict.update({'next_page_number': page_object.next_page_number()})
        if page_object.has_previous():
            page_dict.update({'previous_page_number': page_object.previous_page_number()})
        return  {'page' : page_dict} 
    
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('page_size'):
            self.paginate_by = int(request.GET['page_size'])
        return super(SongListView, self).get(request, *args, **kwargs)
    
    def render_to_response(self, context):
        context.update({'page_class':'paginated"'})
        print "render enter!"
        r = self.request
        #print r
        if not r.POST:
            #print "GEt"
            search = r.GET.get(u'search')
            if (r.GET.has_key('options')):
                opts=r.GET['options']
            else:
                opts='A'            
            if search:
                search_terms = str(r.GET.get(u'search')).split()
                self.queryset = self.search(search_terms, opts, self.model.objects)
            else:
                search=''
                self.queryset = self.model.objects.all()
            print "continue"
            paginator, page, paginated_list, isp = self.paginate_queryset(self.queryset, self.paginate_by)
            xhr = r.GET.has_key('xhr')
            if xhr:
                print "is_ajax"
                response_dict = {}
                t = loader.get_template('SongManager/songs.html')
                #print "loader"
                c = Context({'song_list': paginated_list})
                #print "context"
                
                c.update(self.get_Page_dictionary(page))
                #print "context2"
                c.update({'search': search})
                #print c
                songdata = t.render(c)
#                print songdata
                response_dict.update(self.get_Page_dictionary(page))
                #print paginated_list.values()
                #print serializers.serialize('json', paginated_list, use_natural_keys=true)
                #print serializers.serialize('json', paginated_list, indent=4, relations={'composers':{'extras':('__unicode__',)},},\
                 #                           extras=('__unicode__','get_absolute_url'))
                response_dict.update({
                                      'songs': songdata,
                                      'songs_json': serializers.serialize('json', paginated_list, indent=4,\
                                            relations={'composers':{'extras':('__unicode__',)},},\
                                            extras=('__unicode__','get_absolute_url', 'get_delete_url', 'get_update_url')),
                                      'edit_perm': r.user.has_perm('SongManager.change_song'),
                                      'delete_perm': r.user.has_perm('SongManager.delete_song'),
                                      'search': search,
                                      'search_url': reverse('song_list_view'),
                                      'option': opts,
                                    })
                
                return JSONResponseMixin.render_to_response(self, response_dict)
            form = SearchForm(initial={'search': search,
                                       'options':opts}).as_p()
            
            context.update({'search_form': form,})
            context.update(self.get_Page_dictionary(page))
            context.update({'search': search,
                            'option':opts,})
            context.update({'song_list': paginated_list})
            return ListView.render_to_response(self, context)
        else:
            # post handling here
            return super(SongListView, self).render_to_response(context)


class JSONSongListView(SongListView):
    paginate_by = None
    def render_to_response(self, context):
        limit = 10
        start = 0
        r = self.request
        if not r.POST:
            search = r.GET.get(u'search')
            q = None
            if (r.GET.has_key('options')):
                opts=r.GET['options']
            else:
                opts='A'
            if r.GET.has_key('limit'):
                limit = int(r.GET['limit'])
            if r.GET.has_key('start'):
                start = int(r.GET['start'])      
            if search:
                search_terms = str(r.GET.get(u'search')).split()
                if limit>0:
                    
                    q = self.search(search_terms, opts, self.model.objects)
                    print "length: "+str(len(q))
                    self.queryset = q[start:start+limit]
                    print "returning len "+str(len(self.queryset))
                else:
                    self.queryset = self.search(search_terms, opts, self.model.objects)
                    q = self.queryset
            else:
                search=''
                if limit>0:
                    print limit
                    q = self.model.objects.all()
                    self.queryset = q[start:start+limit]
                else:
                    self.queryset = self.model.objects.all()
                    q = self.queryset

            print self.queryset
            response_dict = {}

            response_dict.update({ 
                                  'songs_json': serializers.serialize('json', self.queryset, indent=4,\
                                        relations={'composers':{'extras':('__unicode__',)},},\
                                        extras=('__unicode__','get_absolute_url', 'get_delete_url', 'get_update_url')),
                                  'search': search,
                                  'search_url': reverse('song_list_view'),
                                  'option': opts,
                                  'count': len(q)
                                })
            
            return JSONResponseMixin.render_to_response(self, response_dict)

        else:
            return super(SongListView, self).render_to_response(context)
            
class SongCreateView(CreateView):
    model = Song
    form_class=SongForm
    def get_context_data(self, **kwargs):
        context = super(SongCreateView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongCreate'})
        return context    
    @method_decorator(permission_required('SongManager.add_song'))
    def dispatch(self, *args, **kwargs):
        return super(SongCreateView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('song_update_view', args=(self.object.pk,))

class SongDeleteView(DeleteView):
    model = Song
    def get_context_data(self, **kwargs):
        context = super(SongDeleteView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongDelete'+str(self.object.pk)})
        return context
    @method_decorator(permission_required('SongManager.delete_song'))
    def dispatch(self, *args, **kwargs):
        return super(SongDeleteView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('song_list_view')

class SongFileDeleteView(DeleteView):
    model = SongFile
    def get_context_data(self, **kwargs):
        context = super(SongFileDeleteView, self).get_context_data(**kwargs)
        context.update({
                        'page_id':'SongFileDelete'+str(self.object.pk)})
        return context    
    @method_decorator(permission_required('SongManager.delete_songfile'))
    def dispatch(self, *args, **kwargs):
        return super(SongFileDeleteView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        pk = self.kwargs.get('song_pk', None)
        return reverse('song_update_view', args=(pk,))
    def render_to_response(self, context):
        pk =  self.kwargs.get('pk', None)
        song = Song.objects.get(songfile__pk=pk)
        context.update({'song_pk':song.pk})
        return super(SongFileDeleteView, self).render_to_response(context)

#########################################
# other views

def JSONFileTypeListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        filetypes = FileType.objects.filter(type__icontains=term) 
    else:
        filetypes = FileType.objects.all()
    filetype_list = []
    for filetype in filetypes:
        filetype_list.append(smart_unicode(filetype))
        
    response = HttpResponse(json.dumps(filetype_list,  ensure_ascii=False))
    return response


def JSONComposerListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        composers = Composer.objects.filter(Q(first_name__icontains=term)|Q(last_name__icontains=term)) 
    else:
        composers = Composer.objects.all()
    composer_list = []
    for composer in composers:
        composer_list.append(smart_unicode(composer))
        
    response = HttpResponse(json.dumps(composer_list,  ensure_ascii=False))
    return response
