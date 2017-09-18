from django.conf.urls import patterns, url
#from django.views.generic import ListView
from models import Song
from views import  SongFileDeleteView, SongDeleteView, SongCreateView, SongDetailView, SongUpdateView, SongUploadView, SongListView,\
    JSONSongListView, JSONFileTypeListView,REST_songfile_filetype_view, REST_songfile_view
#from django.core.urlresolvers import reverse

urlpatterns = patterns('SongManager.views',
    url(r'^generic/$', SongListView.as_view(), name="old_song_list_view"),
    url(r'^generic/(?P<pk>\d+)/$', SongDetailView.as_view(), name="old_song_detail_view" ),
    url(r'^generic/create/$', SongCreateView.as_view(), name='old_song_create_view' ),
    url(r'^generic/(?P<pk>\d+)/update/$', SongUpdateView.as_view(), name='old_song_update_view'),
    url(r'^generic/(?P<pk>\d+)/delete/$', SongDeleteView.as_view(), name='old_song_delete_view'),
    url(r'^generic/(?P<song_pk>\d+)/deletefile/(?P<pk>\d+)$', SongFileDeleteView.as_view(), name='old_songfile_delete_view'),
    url(r'^generic/(?P<pk>\d+)/upload/$', SongUploadView.as_view(), name='old_song_upload_view'),
    url(r'^$', SongListView.as_view(), name="song_list_view"),
    url(r'^(?P<pk>\d+)/$', SongDetailView.as_view(), name="song_detail_view" ),
    url(r'^create/$', SongCreateView.as_view(), name='song_create_view' ),
    url(r'^(?P<pk>\d+)/update/$', SongUpdateView.as_view(), name='song_update_view'),
    url(r'^(?P<pk>\d+)/delete/$', SongDeleteView.as_view(), name='song_delete_view'),
    url(r'^(?P<song_pk>\d+)/deletefile/(?P<pk>\d+)$', SongFileDeleteView.as_view(), name='songfil\
e_delete_view'),
    url(r'^(?P<pk>\d+)/upload/$', SongUploadView.as_view(), name='song_upload_view'),
    url(r'^rest/$', JSONSongListView.as_view(), name='json_songlist_view'),
    url(r'^rest/filetypes/$', JSONFileTypeListView, name='json_filetypelist_view'),
    url(r'^rest/songfiles/(?P<songfile_id>\d+)$', REST_songfile_view, name='rest_songfile_view'),
    url(r'^rest/songfiles/(?P<songfile_id>\d+)/(?P<songtype>[\w_-]+)$', REST_songfile_filetype_view, name='rest_songfile_filetype_view'),
)
