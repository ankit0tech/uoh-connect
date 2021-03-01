from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.CreatePost.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdatePost.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete'),
    path('list/', views.PostList.as_view(), name='list'),
    path('details/<int:pk>/', views.post_detail, name='details'),
    # urls for comment
    path('<int:pk>/create-comment/', views.CreateComment.as_view(), name='create_comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]