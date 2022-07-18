from django.urls import path

from categories.views import *

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/', CategoryEntityView.as_view(), name='category'),
    path('create/', CategoryCreateView.as_view(), name='create category'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='update category'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete category'),
    ]