from django.conf.urls import url
from . import views
from django.urls import path,include

app_name = 'music'

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    # url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    # url(r'^create_album/$', views.create_album, name='create_album'),
    # url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    # url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    # url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    # url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    path('(<album_id>[0-9]+)/', views.detail, name='detail'),
    path('(<song_id>[0-9]+)/favorite/', views.favorite, name='favorite'),
    path('songs/(<filter_by>[a-zA_Z]+)/', views.songs, name='songs'),
    path('create_album/', views.create_album, name='create_album'),
    path('(<album_id>[0-9]+)/create_song/', views.create_song, name='create_song'),
    path('(<album_id>[0-9]+)/delete_song/(<song_id>[0-9]+)/', views.delete_song, name='delete_song'),
    path('(<album_id>[0-9]+)/favorite_album/', views.favorite_album, name='favorite_album'),
    path('(<album_id>[0-9]+)/delete_album/', views.delete_album, name='delete_album'),
]
