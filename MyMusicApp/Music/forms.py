from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Artist, Album, Year, Genre, Music


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ArtistCreateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['artist_name', 'bio', 'artist_image']


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        # widgets = {
        #     'birth_date': forms.TextInput(attrs={'placeholder': '1992-02-19'}),
        # }
        fields = ['artist', 'title', 'genre', 'year']


class MusicCreateForm(forms.ModelForm):
    class Meta:
        model = Music

        fields = ['title', 'artist', 'year', 'album', 'genre', 'media', 'image_art']





