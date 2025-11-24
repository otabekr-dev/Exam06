from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        