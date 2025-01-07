from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('myads/', views.MyAdsView.as_view(), name='my_ads'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('ad/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    path('sponsored/', views.sponsored_ads, name='sponsored_ads'),
] 