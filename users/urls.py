from django.urls import path

from users.views import *

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/', UserDetailView.as_view(), name='user'),
    path('create/', UserCreateView.as_view(), name='create user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update user'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete user'),
    ]