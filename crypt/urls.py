from django.conf.urls import url
from crypt import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^history/$', views.history_page, name='history_page'),
    url(r'^create_post/(?P<pk>[0-9]+)/$',
        views.create_post, name='create_post'),
    url(r'^decrypt_post/(?P<pk>[0-9]+)/$',
        views.decrypt_post, name='decrypt_post'),

]
