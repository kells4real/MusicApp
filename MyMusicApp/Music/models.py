from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


def get_music_filename(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "music/{}/{}".format(slug, filename)


def get_art_filename(instance, filename):
    title = instance.artist_name
    slug = slugify(title)
    return "pic/artist_pic/{}/{}".format(slug, filename)


def get_album_art_filename(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "pic/album_pic/{}/{}".format(slug, filename)


def get_music_art_filename(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "pic/music_pic/{}/{}".format(slug, filename)


class PopularArtist(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True, default="Poupular")

    def __str__(self):
        return self.title


class Artist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    artist_name = models.CharField(max_length=50, null=True, blank=True)
    # date_of_birth = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    artist_image = models.ImageField(upload_to=get_art_filename, null=True, blank=True)
    popularity = models.ForeignKey(PopularArtist, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.artist_name

    def _get_unique_slug(self):
        slug = slugify(self.artist_name)
        unique_slug = slug
        num = 1
        while Artist.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

        img = Image.open(self.artist_image.path)

        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.artist_image.path)



class Year(models.Model):
    year = models.CharField(max_length=4, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

    def __str__(self):
        return self.year

    def _get_unique_slug(self):
        slug = slugify(self.year)
        unique_slug = slug
        num = 1
        while Year.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

    def __str__(self):
        return self.genre_name

    def _get_unique_slug(self):
        slug = slugify(self.genre_name)
        unique_slug = slug
        num = 1
        while Genre.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True)
    album_image = models.ImageField(upload_to=get_album_art_filename, null=True, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('home', args=[str(self.id)])

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Album.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

        img = Image.open(self.album_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.album_image.path)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, help_text="Enter Playlist Name")
    date_created = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="playlist")
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Album.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Music(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    media = models.FileField(upload_to=get_music_filename, null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    year = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1980), MaxValueValidator(2050)])
    image_art = models.ImageField(default='default.jpg', upload_to='image_arts')
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
    
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Album.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

        img = Image.open(self.image_art.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image_art.path)





