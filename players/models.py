from django.db import models

# Create your models here.
class Player(models.Model):
    nickname = models.CharField(max_length=50,unique=True)
    country = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
      
    def to_dict(self):
        return {
            "id": self.pk,
            "nickname": self.nickname,
            "country": self.country,
            "rating": self.rating,
            "created_at":self.created_at.isoformat()
        }
    
    def get_score(self):
        total_games = self.scores.count()
        wins = self.scores.filter(result='win').count()
        draws = self.scores.filter(result='draw').count()
        losses = self.scores.filter(result='loss').count()

        return {
            "id": self.pk,
            "nickname": self.nickname,
            "country": self.country,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "total_games": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses
        }