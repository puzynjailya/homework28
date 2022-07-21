from django.urls import path

from advertisements.views import *

urlpatterns = [
    path('', AdsListView.as_view(), name='ads'),
    path('<int:pk>/', AdEntityView.as_view(), name='ad'),
    path('create/', AdCreateView.as_view(), name='create ad'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='update ad'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete ad'),
    path('<int:pk>/upload_image/', AdImageUploadView.as_view(), name='image import')
    ]