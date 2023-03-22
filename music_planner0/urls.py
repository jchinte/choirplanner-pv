from menus.views import MenuListView
from django.urls import re_path
from django.urls import include as old_include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.views import  logout_then_login
admin.autodiscover()
from music_planner0.views import UserCreateView, AdminUserUpdateView, UserDetailView, index, redirect_to_vite
#from dh5bp.urls import urlpatterns as dh5bp_urls
admin.autodiscover()
from django.http import HttpResponse
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from music_planner0 import settings
from django.urls import path, re_path, include
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views as rest_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.core import urls as wagtaildocs_urls
from .api import api_router

urlpatterns = [
    # Examples:
    # url(r'^$', 'newproject.views.home', name='home'),
    # url(r'^newproject/', include('newproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    re_path(r'^admin/doc/', old_include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^songs/', old_include('SongManager.urls')),
    re_path(r'^events/', old_include('Event_Planner.urls')),
    re_path(r'^protected/', include('protected_media.urls')),
    path(r'accounts/', include('django.contrib.auth.urls')),
    # re_path(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^accounts/logout/$', logout_then_login, name='django.contrib.auth.views.logout_then_login'),
    # re_path(r'^accounts/create/$', UserCreateView.as_view()),
    # re_path(r'^accounts/perms/(?P<slug>\w+)/$', AdminUserUpdateView.as_view()),
    re_path(r'^users/(?P<slug>\w+)/$', UserDetailView.as_view()),
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('api/v2/', api_router.urls),
    path('api/menu/', MenuListView.as_view()),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtail_urls)),
    path('pages/', include(wagtail_urls)),
    #url(r'^$', RedirectView.as_view(url="/events")), #TODO: Redirect to https
    # re_path(r'^accounts2/', old_include('registration.backends.admin_approval.urls')),
    # path('accounts/', include('django_registration.backends.activation.urls')),
    re_path(r'^app/.*$', redirect_to_vite, name='vite_redirect'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^blog/.*$', index, name='index'), #TODO: Redirect to https
    re_path(r'^$', index, name='index'), #TODO: Redirect to https
    re_path(r'^___logout/$', auth_views.LogoutView.as_view(), name='account_logout'),
    #url(r'^$', RedirectView.as_view(pattern_name="event_list_view")),
    #(r'^songs/$', 'SongManager.views.index'),
    #(r'^songs/(?P<song_id>\d+)/$', 'SongManager.views.detail'),
    #url(r'^songs/(?P<song_id>\d+)/modify/$', 'SongManager.views.modify', name = 'modify_song'),
    #(r'^songs/search/$', 'SongManager.views.search'),
    #url(r'^songs/add/$', 'SongManager.views.add', name = 'add_new_song'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

#urlpatterns += dh5bp_urls

#handler404 = 'dh5bp.views.page_not_found'
handler500 = 'dh5bp.views.server_error'
