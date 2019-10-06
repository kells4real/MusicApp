from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.storage import default_storage as storage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img_read = storage.open(self.image.name, 'r')
    #     img = Image.open(img_read)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         in_mem_file = io.BytesIO()
    #         img.save(in_mem_file, format='JPEG')
    #         img_write = storage.open(self.image.name, 'w+')
    #         img_write.write(in_mem_file.getvalue())
    #         img_write.close()
    #
    #     img_read.close()


class UserImage(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=True)
    myimage = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.author.username} image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.myimage.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.myimage.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()

