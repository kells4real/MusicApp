from django.shortcuts import render
from .models import Artist, Music, Year, Album, Genre, PopularArtist, Playlist
from .forms import AlbumCreateForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
import random as ran


class MusicView(ListView):
    model = Music
    template_name = 'music/index.html'


def home(request):
    bestest = Playlist.objects.get(slug='trending')
    trending = bestest.music_set.all()[:ran.randint(2, 5)]
    feat = PopularArtist.objects.get(title='Popular')
    p_artist = feat.artist_set.all()

    context = {
        'songs': Music.objects.all().order_by('-date_created')[:6],
        'album': Album.objects.all(),
        # 'feat': feat,
        'p_artist': p_artist,
        'bestest': bestest,
        'trending': trending
    }
    return render(request, 'music/index.html', context)


def album_list(request):
    album = Album.objects.all().order_by('-date_created')
    context = {
        'album': album
    }
    return render(request, 'music/album_list.html', context)


class MusicDetail(DetailView):
    model = Music


# def album_create(request):
#     form = AlbumCreateForm()
#     return render(request, 'App/scores_new.html', {'form': form})


def playlist_detail(request, slug):
    context = {
        'play': Playlist.objects.get(slug=slug)

    }
    return render(request, 'music/playlist_detail.html', context)


def album_detail(request, slug):
    context = {
        'album': Album.objects.get(slug=slug)
    }
    return render(request, 'music/album_detail.html', context)


def artist_detail(request, slug):
    artist = Artist.objects.get(slug=slug)
    all_albums = artist.album_set.all()
    count = 0

    for album in all_albums:
        count = count + 1

    context = {
        'artist': artist,
        'all_albums': all_albums,
        'count': count

    }
    return render(request, 'music/artist_detail.html', context)


def contact(request):
    return render(request, 'music/contact.html')


