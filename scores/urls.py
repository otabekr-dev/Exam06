from django.urls import path
from .views import ScoreView, DetailedScoreView

urlpatterns = [
    path('scores/', ScoreView.as_view(), name='scores'),
    path('scores/<int:pk>/',DetailedScoreView.as_view(), name='scores-detailed')
]