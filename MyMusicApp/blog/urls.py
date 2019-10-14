from django.urls import path

from . import views
from datetime import date # This to give every create post link a unique url



urlpatterns = [
    path('', views.post_list, name='blog-home'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),
    path('<slug>/', views.post_detail, name='post-detail'),
    path('category/<slug>/', views.category_list, name='category-list'),
    path(f'{date.today()}/new', views.PostCreateView.as_view(), name='post-create'), # Dynamic post create url
    path('post/<slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('edit_comment/<int:pk>', views.CommentUpdateView.as_view(), name='comment-edit'),
    path('edit_commentreply/<int:pk>', views.CommentReplyUpdateView.as_view(), name='commentreplyedit'),
    path('about/', views.about, name='blog-about'),
    path('commentreplydelete/<int:pk>', views.CommentReplyDelete.as_view(), name='commentreplydelete'),
    path('commentdelete/<int:pk>', views.CommentDelete.as_view(), name='commentdelete'),
    path('update/<slug>/', views.PostUpdateView.as_view(), name='post-update'),
    path('delete/<slug>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/search/', views.SearchResultsView.as_view(), name='search'),
]
