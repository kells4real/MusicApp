from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from users.models import UserImage


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Hashtag.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)



def image_upload(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "posts/{}/{}".format(slug, filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True, default='default.jpg')
    image_2 = models.ImageField(upload_to=image_upload, null=True, blank=True)
    category = models.ForeignKey(Hashtag, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 900 or img.width > 1200:
            output_size = (900, 1200)
            img.thumbnail(output_size)
            img.save(self.image.path)



class Comment(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    usrimg = models.ForeignKey(UserImage, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.message



class CommentReply(models.Model):
    whichcomment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    usrimg = models.ForeignKey(UserImage, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.message

