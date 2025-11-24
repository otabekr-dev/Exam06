import json

from django.views import View
from .models import Game
from django.http import HttpRequest, JsonResponse


class GameListView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        
        games = [
            {
                "game_id": game.pk,
                "title": game.title,
                "location": game.location,
                "start_date": game.start_date,
                "description": game.description,
                "created_at": game.created_at,
            }
            for game in Game.objects.all()
        ]
        return JsonResponse({"games": games})   
    

    def post(self, request: HttpRequest) -> JsonResponse:

        data = json.loads(request.body)

        name = data.get('title')
        if not name:
            return JsonResponse({'title': 'Required.'}, status=400)
        elif len(name) > 200:
            return JsonResponse({'title': 'Max 200 characters.'}, status=400)
        

       
        game = Game.objects.create(
            title=data.get("title"),
            location=data.get("location"),           
            start_date=data.get("start_date"),
            description=data.get("description"),
        )
        game.save()
        return JsonResponse({
            "game_id": game.pk,
            "title": game.title,
            "location": game.location,
            "start_date": game.start_date,
            "description": game.description,
            "created_at": game.created_at.isoformat(),
        })
    
class GameDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)
        
        return JsonResponse({
            "game_id": game.pk,
            "title": game.title,
            "location": game.location,
            "start_date": game.start_date,
            "description": game.description,
            "created_at": game.created_at,
        })
    
    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)
        
        data = json.loads(request.body) if request.body else {}

        

        game.title = data.get("title", game.title)
        game.location = data.get("location", game.location)
        game.start_date = data.get("start_date", game.start_date)
        game.description = data.get("description", game.description)
        game.save()
        
        return JsonResponse({
            "game_id": game.pk,
            "title": game.title,
            "location": game.location,
            "start_date": game.start_date,
            "description": game.description,
            "created_at": game.created_at,
        })
    
    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return JsonResponse({'message': 'Game deleted successfully.'})
        
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)
