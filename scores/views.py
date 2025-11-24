import json
from django.views import View
from django.http import HttpRequest, JsonResponse
from .models import Score
from players.models import Player
from games.models import Game


class ScoreView(View):
    
    def get(self, request: HttpRequest) -> JsonResponse:
        scores = Score.objects.all()
        game_id = request.GET.get('game_id')
        player_id = request.GET.get('player_id')
        result = request.GET.get('result')

        if game_id:
            scores = scores.filter(game_id=game_id)
        if player_id:
            scores = scores.filter(player_id=player_id)
        if result:
            scores = scores.filter(result=result)

        data = [
            {
                "id": s.pk,
                "game": {"id": s.game.pk, "title": s.game.title},
                "player": {"id": s.player.pk, "nickname": s.player.nickname},
                "result": s.result,
                "points": s.points,
                "opponent_name": s.opponent_name,
                "created_at": s.created_at.isoformat()
            }
            for s in scores
        ]
        return JsonResponse({"results": data})

    def post(self, request:HttpRequest) -> JsonResponse:
        data = json.loads(request.body)

        player = Player.objects.get(pk=data['player'])
        game = Game.objects.get(pk=data['game'])

        score = Score.objects.create(
            game=game,
            player=player,
            result=data['result'],      
            opponent_name=data.get('opponent_name')
        )

        return JsonResponse({
            "id": score.pk,
            "game": {"id": game.pk, "title": game.title},
            "player": {"id": player.pk, "nickname": player.nickname},
            "result": score.result,
            "points": score.points,
            "opponent_name": score.opponent_name,
            "created_at": score.created_at.isoformat()
        }, status=2)

class DetailedScoreView(View):
    
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            s = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return JsonResponse({'error': 'Score not found'}, status=404)

        return JsonResponse({
            "id": s.pk,
            "game": {"id": s.game.pk, "title": s.game.title, "location": s.game.location},
            "player": {"id": s.player.pk, "nickname": s.player.nickname, "country": s.player.country},
            "result": s.result,
            "points": s.points,
            "opponent_name": s.opponent_name,
            "created_at": s.created_at.isoformat()
        })

    def delete(self, request: HttpRequest, pk:int) -> JsonResponse:
        try:
            s = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return JsonResponse({'error': 'Score not found'}, status=404)

        player = s.player
        s.delete()
      
        player.rating = sum(score.points for score in player.scores.all())
        player.save()
        return JsonResponse({}, status=204)

