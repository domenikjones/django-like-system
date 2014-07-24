from django.conf.urls import patterns, url


urlpatterns = patterns('like_system.views',
    url(r'unlike/(?P<content_type>\w+)/(?P<object_pk>[0-9]+)', 'unlike', name='like_system-unlike'),
    url(r'like/(?P<content_type>\w+)/(?P<object_pk>[0-9]+)', 'like', name='like_system-like'),
)