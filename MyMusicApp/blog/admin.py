from django.contrib import admin
from .models import Post, Hashtag, Comment, CommentReply


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class HashtagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Comment)
admin.site.register(CommentReply)