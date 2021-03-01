from django.urls import path
from department import views

app_name = 'department'

urlpatterns = [
    path('list/', views.dept_list, name='list'),
    path('details/<int:pk>/', views.dept_details, name='details'),
    path('posts/<int:pk>/', views.dept_posts, name='posts'),
    path('students/<int:pk>/', views.dept_students, name='students'),
]