from __future__ import unicode_literals
from django.urls import re_path
#from django.views.generic import ListView
from SongManager.models import Song
from SongManager.views import  SongFileDeleteView, SongDeleteView, SongCreateView, SongDetailView, SongUpdateView, SongUploadView, SongListView,\
    JSONSongListView, JSONFileTypeListView,REST_songfile_filetype_view, REST_songfile_view
#from django.core.urlresolvers import reverse
from django.urls import path, include
from rest_framework import routers
from .views import SongFileAPIViewSet, SongAPIViewSet, TagAPIViewSet, FileTypeAPIViewSet

router = routers.DefaultRouter()
router.register(r'api/upload', SongFileAPIViewSet)
router.register(r'api/songs', SongAPIViewSet)
router.register(r'api/tags', TagAPIViewSet)
router.register(r'api/filetypes', FileTypeAPIViewSet)
urlpatterns = [
    re_path(r'^generic/$', SongListView.as_view(), name="old_song_list_view"),
    re_path(r'^generic/(?P<pk>\d+)/$', SongDetailView.as_view(), name="old_song_detail_view" ),
    re_path(r'^generic/create/$', SongCreateView.as_view(), name='old_song_create_view' ),
    re_path(r'^generic/(?P<pk>\d+)/update/$', SongUpdateView.as_view(), name='old_song_update_view'),
    re_path(r'^generic/(?P<pk>\d+)/delete/$', SongDeleteView.as_view(), name='old_song_delete_view'),
    re_path(r'^generic/(?P<song_pk>\d+)/deletefile/(?P<pk>\d+)$', SongFileDeleteView.as_view(), name='old_songfile_delete_view'),
    re_path(r'^generic/(?P<pk>\d+)/upload/$', SongUploadView.as_view(), name='old_song_upload_view'),
    re_path(r'^$', SongListView.as_view(), name="song_list_view"),
    re_path(r'^(?P<pk>\d+)/$', SongDetailView.as_view(), name="song_detail_view" ),
    re_path(r'^create/$', SongCreateView.as_view(), name='song_create_view' ),
    re_path(r'^(?P<pk>\d+)/update/$', SongUpdateView.as_view(), name='song_update_view'),
    re_path(r'^(?P<pk>\d+)/delete/$', SongDeleteView.as_view(), name='song_delete_view'),
    re_path(r'^(?P<song_pk>\d+)/deletefile/(?P<pk>\d+)$', SongFileDeleteView.as_view(), name='songfil\
e_delete_view'),
    re_path(r'^(?P<pk>\d+)/upload/$', SongUploadView.as_view(), name='song_upload_view'),
    re_path(r'^rest/$', JSONSongListView.as_view(), name='json_songlist_view'),
    re_path(r'^rest/filetypes/$', JSONFileTypeListView, name='json_filetypelist_view'),
    re_path(r'^rest/songfiles/(?P<songfile_id>\d+)$', REST_songfile_view, name='rest_songfile_view'),
    re_path(r'^rest/songfiles/(?P<songfile_id>\d+)/(?P<songtype>[\w_-]+)$', REST_songfile_filetype_view, name='rest_songfile_filetype_view'),
    path(r'', include(router.urls)),
]
