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
    objects = Post.objects.get(slug=slug)
    posts = Post.objects.all().order_by('-date_posted')
    side_posts = posts[:3]
    com = Comment.objects.filter(blog=objects)
    com_count = com.all()
    replycom = CommentReply.objects.filter(blog=objects)
    reply_count = replycom.all()
    replycom2 = CommentReply.objects.filter(blog=objects)
    form1 = CommentForm
    form2 = CommentReplyForm

    count = 0
    for num in com_count:
        if num.approved == True:
            count = count + 1

    count2 = 0
    for num in reply_count:

        count2 = count2 + 1

    context = {
        'objects': objects,
        'side_posts': side_posts,
        'com': com,
        'replycom': replycom,
        'replycom2': replycom2,
        'form1': form1,
        'form2': form2,
        'count': count,
        'count2': count2
    }
    if request.method == 'POST':

        if request.POST.get('whichcomment'):
            data3 = CommentReplyForm(request.POST)

            if data3.is_valid():
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

    # model = Post
    # fields = ['title', 'image', 'date_posted', 'content', 'image_2', 'category']
    # template_name = "blog/post_create.html"
    # #
    # # def form_valid(self, form):
    # #     form.instance.author = self.request.user
    # #     return super().form_valid(form)
    # #
    # # def get_success_url(self):
    # #     return reverse_lazy('post-detail', kwargs={'slug': self.object.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'date_posted', 'content', 'image_2', 'category']
    template_name = "blog/post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # def get_context_data(self, **kwargs):
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class CommentReplyDelete(DeleteView):
    model = CommentReply
    template_name = 'blog/blogdelete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'slug': self.object.whichcomment.blog.slug})


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'blog/blogdelete.html'

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