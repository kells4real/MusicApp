from django.contrib import admin
from django.urls import path
from .views import MusicView, home, MusicDetail, album_detail, playlist_detail, artist_detail, album_list, contact

urlpatterns = [
    path('', home, name='home'),
    path('music/<slug:slug>/', MusicDetail.as_view(), name='music-detail'),
    path('album/<slug:slug>/', album_detail, name='album-detail'),
    path('playlist/<slug:slug>/', playlist_detail, name='playlist-detail'),
    path('artist/<slug:slug>/', artist_detail, name='artist-detail'),
    path('albums/', album_list, name='album-list'),
    path('contact/', contact, name='contact'),
]
