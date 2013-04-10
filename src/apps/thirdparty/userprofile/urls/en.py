from django.conf.urls import *
from django.views.generic import TemplateView
from apps.thirdparty.userprofile.views import *
from django.conf import settings

urlpatterns = patterns('',
    # Private profile
    url(r'^$', overview, name='profile_overview'),

    url(r'^edit/location/$', location, name='profile_edit_location'),

    url(r'^edit/location/done/$', TemplateView.as_view(template_name="userprofile/profile/location_done.html"),
        {'extra_context': {'section': 'location'}}, name='profile_edit_location_done'),

    url(r'^edit/personal/$', personal, name='profile_edit_personal'),

    url(r'^edit/personal/done/$', TemplateView.as_view(template_name="userprofile/profile/personal_done.html"),
        {'extra_context': {'section': 'personal'}},
        name='profile_edit_personal_done'),

    url(r'^delete/$', delete, name='profile_delete'),

    url(r'^delete/done/$', TemplateView.as_view(template_name="userprofile/profile/delete_done.html"),
        {'extra_context': {'section': 'delete'}},
        name='profile_delete_done'),

    url(r'^getcountry_info/(?P<lat>[0-9\.\-]+)/(?P<lng>[0-9\.\-]+)/$',
        fetch_geodata,
        name='profile_geocountry_info'),

    # Avatars
    url(r'^edit/avatar/delete/$', avatardelete,
        name='profile_avatar_delete'),

    url(r'^edit/avatar/$', avatarchoose, name='profile_edit_avatar'),

    url(r'^edit/avatar/search/$', searchimages,
        name='profile_avatar_search'),

    url(r'^edit/avatar/crop/$', avatarcrop,
        name='profile_avatar_crop'),

    url(r'^edit/avatar/crop/done/$', TemplateView.as_view(template_name="userprofile/avatar/done.html"), {'extra_context': {'section': 'avatar'}}, name='profile_avatar_crop_done'),

    # Account utilities
    url(r'^email/validation/$', email_validation, name='email_validation'),

    url(r'^email/validation/processed/$', TemplateView.as_view(template_name="userprofile/account/email_validation_processed.html"),
        name='email_validation_processed'),

    url(r'^email/validation/(?P<key>.{70})/$', email_validation_process,
        name='email_validation_process'),

    url(r'^email/validation/reset/$', email_validation_reset,
        name='email_validation_reset'),

    url(r'^email/validation/reset/(?P<action>done|failed)/$',
        TemplateView.as_view(template_name="userprofile/account/email_validation_reset_response.html"),
        name='email_validation_reset_response'),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'userprofile/account/password_reset.html',
         'email_template_name': 'userprofile/email/password_reset_email.txt'},
        name='password_reset'),

    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'userprofile/account/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^password/change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'userprofile/account/password_change.html'},
        name='password_change'),

    url(r'^password/change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'userprofile/account/password_change_done.html'},
        name='password_change_done'),

    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'userprofile/account/password_reset_confirm.html'},
        name="password_reset_confirm"),

    url(r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'userprofile/account/password_reset_complete.html'},
        name="password_reset_complete"),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'userprofile/account/login.html'},
        name='login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'userprofile/account/logout.html'},
        name='logout'),

    url(r'^email/change$', email_change, name='email_change'),

    # Registration
    url(r'^register/$', register, name='signup'),

    url(r'^register/validate/$', TemplateView.as_view(template_name="userprofile/account/validate.html"), name='signup_validate'),

    url(r'^register/complete/$', TemplateView.as_view(template_name="userprofile/account/registration_done.html"), name='signup_complete'),

    # Users public profile
    url(r'^(?P<username>.+)/$', public, name='profile_public'),

)
