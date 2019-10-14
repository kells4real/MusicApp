from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CommentForm, CommentReplyForm, PostForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, CommentReply, Comment, UserImage, Hashtag
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    side_posts = posts[:3]

    context = {
        'posts': posts,
        'side_posts': side_posts
    }
    return render(request, 'blog/home.html', context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# class PostDetailView(DetailView):
#     model = Post

def post_detail(request, slug):
    objects = Post.objects.get(slug=slug)  # Get a specific post based on slug field
    posts = Post.objects.all().order_by('-date_posted') # All Posts
    side_posts = posts[:3] # Posts limited to 3
    com = Comment.objects.filter(blog=objects) # Get comments based on a specific post
    com_count = com.all() # All Comments for the specific Post.. If I was going to
    # place the number of comments in the for loop that loops over all comments,
    # it would have been easy as just {% for comment in com %} {{ comment.message.count }}
    replycom = CommentReply.objects.filter(blog=objects) # comment reply related to a specific Post
    reply_count = replycom.all()
    # replycom2 = CommentReply.objects.filter(blog=objects)
    form1 = CommentForm
    form2 = CommentReplyForm
    category = Hashtag.objects.all()
    com_count2 = com_count.count() # This is only here to show my students how we could do it differently



    search_list = ["fuck", "shit", "fucked", "fucking",
                   "mother fucker", "mother fucker", "fuck you",
                    "fucked", "shit", "asshole", "ass hole", "nigga",
                   "niggro", "ass"] # List of words that should not be used whe n making a comment.

    for mess in com_count: # Checks for foul words in comments and deletes any comment found wanting..
        if any(c in mess.message.casefold() for c in search_list):
            mess.delete()
            messages.success(request, f'Your comment was deleted because it contained fowl words or language..')

    for mess in reply_count: # Checks for foul words in comments reply and deletes any comment found wanting..
        if any(c in mess.message.casefold() for c in search_list):
            mess.delete()
            messages.success(request, f'Your comment was deleted because it contained fowl words or language..')


    context = {
        'objects': objects,
        'side_posts': side_posts,
        'com': com,
        'replycom': replycom,
        'form1': form1,
        'form2': form2,
        'com_count2': com_count2, # This is only here to show my students how we could do it differently
        'url': "post-detail", # This is to differentiate between messages on post detail page from other pages in the base.html
        'category': category,

    }
    if request.method == 'POST':

        if request.POST.get('whichcomment'):
            data3 = CommentReplyForm(request.POST) # Assigned CommentReplyForm to data3

            if data3.is_valid(): # if form is valid
                whichcomment = int(request.POST.get('whichcomment'))
                message = data3.cleaned_data['message']
                #                user = User.objects.get(username=request.user.username)
                #                usrimg = UserImage.objects.get(author=user)

                don = data3.save(commit=False)
                don.blog = objects
                don.user = User.objects.get(username=request.user.username)
                don.message = message
                don.whichcomment = Comment.objects.get(id=whichcomment)
                don.usrimg = UserImage.objects.get(author=don.user)
                don.save()

                return HttpResponseRedirect(reverse('post-detail', args=(), kwargs={'slug': slug}))

        else:
            data2 = CommentForm(request.POST)

            if data2.is_valid():
                blog = objects
                message = data2.cleaned_data['message']
                #                usr = User.objects.get(user=request.user.username),
                #                usrimg = UserImage.objects.get(author=usr)

                don = data2.save(commit=False)
                don.blog = objects
                don.user = User.objects.get(username=request.user.username)
                don.message = message
                don.usrimg = UserImage.objects.get(author=don.user)
                don.save()

                '''Comment.objects.create(
                    blog=data1,
                    user= User.objects.get(username=request.user.username),
                    message=message,
                    usrimg=UserImage.objects.get(author=user)

                ).save()'''

                return HttpResponseRedirect(reverse('post-detail', args=(), kwargs={'slug': slug}))

    else:
        return render(request, 'blog/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': PostForm()}
        return render(request, 'blog/post_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = self.request.user
            post = form.save()
            post.save()
            return HttpResponseRedirect(reverse_lazy('post-detail', args=[post.slug]))
        return render(request, 'blog/post_create.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'date_posted', 'content', 'image_2', 'category', 'display_comment']
    template_name = "blog/post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/post/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class CommentReplyDelete(DeleteView):
    model = CommentReply
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.whichcomment.blog.slug})


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.blog.slug})



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['message']
    template_name = 'blog/comment_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.blog.slug})


class CommentReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommentReply
    fields = ['message']
    template_name = 'blog/comment_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.whichcomment.blog.slug})


def category_list(request, slug):
    post = Hashtag.objects.get(slug=slug)
    posts = post.post_set.all()
    context = {
        'posts': posts,
        'post':post
    }
    return render(request, 'blog/category_list.html', context)