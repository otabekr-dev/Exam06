from django.urls import path
from .views import GameListView, GameDetailView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
]