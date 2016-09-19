from django.conf.urls import url
from crypt import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^decrypt/$', views.decrypt_page, name='decrypt_page'),
    url(r'^history/$', views.history_page, name='history_page'),
    url(r'^create_post/$', views.create_post, name='create_post'),

]
