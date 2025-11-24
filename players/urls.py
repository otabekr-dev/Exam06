from django.urls import path

from .views import PlayerView, DetailedPlayerView

urlpatterns = [
    path('players/',PlayerView.as_view(),name='players'),
    path('players/<int:pk>/', DetailedPlayerView.as_view())
]