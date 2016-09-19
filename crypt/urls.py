from django.conf.urls import url
from crypt import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^create_post/$', views.create_post, name='create_post'),

]
