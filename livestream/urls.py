from django.urls import path, include
from livestream import views


urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('eyedet_feed', views.eyedet_feed, name='eyedet_feed'),
    ]
