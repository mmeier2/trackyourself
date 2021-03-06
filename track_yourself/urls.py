
from django.conf.urls import patterns, include, url
from track_yourself.views import home, Login, register, login_auth, log_phys_data, log_workout, view_summary, register_auth, user_home, access_denied, logout, invalid_login, add_data, view_data_summary, create_csv, add_doctor, email_doc
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# 
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$'			   , home),
    url(r'^$'			   , home),
    url(r'^home/Login.html$'			   , Login),
    url(r'^Login.html$'			   , Login),
    url(r'^home/register.html$'			   , register),
    url(r'^register.html$'			   , register),
 	url(r'^home/login_auth/$', 					login_auth),
 	url(r'^login_auth/$', 					login_auth), 	
 	url(r'^home/register_auth/$', 					register_auth),
 	url(r'^register_auth/$', 					register_auth), 	
 	url(r'^phys_data/$'			   , log_phys_data),
 	url(r'^home/phys_data/$'			   , log_phys_data),
 	url(r'^workout/$'			   , log_workout),
 	url(r'^home/workout/$'			   , log_workout),
 	url(r'^home/view_summary/$'			   , view_summary),  	
 	url(r'^view_summary/$'			   , view_summary),
 	url(r'^home/user_home/$'			, user_home),
 	url(r'^user_home/$'					, user_home),
 	url(r'^access_denied/$'					, access_denied),
    url(r'^logout/$'                    ,logout),
    url(r'^home/logout/$'               ,logout),
    url(r'^home/logout/$'               ,logout),
    url(r'^invalid_login/$'               ,invalid_login),
    url(r'^invalid_login/login_auth/$'               ,login_auth),
    url(r'^add_data/$'                          ,add_data), 
    url(r'^view_data_summary/$'             ,view_data_summary),
    url(r'^create_csv/$'             ,create_csv),
    url(r'^add_doctor/$'                ,add_doctor),
    url(r'^email_doc/$'                 , email_doc),  
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
urlpatterns += staticfiles_urlpatterns()
