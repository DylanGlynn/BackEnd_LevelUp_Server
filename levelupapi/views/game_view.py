from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType

class GameView(ViewSet):
    ''' Level Up games view. '''

    def retrieve(self, request, pk):
        ''' Handles GET requests for single game.
        
        Returns:
            Response -- JSON serialized game.
        '''

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        ''' Handles GET requests for all games.
        
        Returns:
            Response -- JSON serialized list of games.
        '''

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


    def create(self, request):
        ''' Handles POST operations.
        
        Returns:
            Response -- JSON serialized game instance.
        '''

        # gamer = Gamer.objects.get(user=request.auth.user)
        # type = GameType.objects.get(pk=request.data['type_id'])

        game = Game.objects.create(
            title=request.data['title'],
            maker=request.data['maker'],
            number_of_players=request.data['number_of_players'],
            skill_level=request.data['skill_level'],
            # gamer=gamer,
            type_id=request.data['type'],
        )
        print(game)
        serializer = GameSerializer(game)
        return Response(serializer.data)


    def update(self, request, pk):
        ''' Handles PUT requests for a game.
        
        Returns:
            Response -- Empty body with 204 status code.
        '''

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["type"])
        game.type_id = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        ''' Handles DELETE requests. '''

        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    ''' JSON serializer for games. '''

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'type')
        depth = 1
