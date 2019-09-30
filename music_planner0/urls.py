from django.conf.urls import  include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
admin.autodiscover()
from music_planner0.views import UserCreateView, AdminUserUpdateView, UserDetailView
#from dh5bp.urls import urlpatterns as dh5bp_urls
admin.autodiscover()
from django.http import HttpResponse
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views





urlpatterns = [
    # Examples:
    # url(r'^$', 'newproject.views.home', name='home'),
    # url(r'^newproject/', include('newproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^songs/', include('SongManager.urls')),
    url(r'^events/', include('Event_Planner.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/create/$', UserCreateView.as_view()),
    url(r'^accounts/perms/(?P<slug>\w+)/$', AdminUserUpdateView.as_view()),
    url(r'^users/(?P<slug>\w+)/$', UserDetailView.as_view()),
    url(r'^$', RedirectView.as_view(url="https://praisingvoices.org/blog")),
    #url(r'^$', RedirectView.as_view(pattern_name="event_list_view")),
    url(r'^accounts2/', include('registration.backends.admin_approval.urls')),
    #(r'^songs/$', 'SongManager.views.index'),
    #(r'^songs/(?P<song_id>\d+)/$', 'SongManager.views.detail'),
    #url(r'^songs/(?P<song_id>\d+)/modify/$', 'SongManager.views.modify', name = 'modify_song'),
    #(r'^songs/search/$', 'SongManager.views.search'),
    #url(r'^songs/add/$', 'SongManager.views.add', name = 'add_new_song'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#urlpatterns += dh5bp_urls

#handler404 = 'dh5bp.views.page_not_found'
handler500 = 'dh5bp.views.server_error'
