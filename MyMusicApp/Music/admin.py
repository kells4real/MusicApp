from django.contrib import admin
from .models import Year, Album, Artist, Genre, Music, Playlist, PopularArtist

# Register your models here.


class YearAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("year",)}


class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("artist_name",)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("genre_name",)}
    

class MusicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PlaylistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(PopularArtist)
