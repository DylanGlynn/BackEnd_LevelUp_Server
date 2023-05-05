from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Gamer, Game

class EventView(ViewSet):
    ''' Level Up event view. '''

    def retrieve(self, request, pk):
        ''' Handles GET requests for a single event.
        
        Returns:
            Response -- JSON serialized event.
        '''

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        ''' Handles GET requests for all events.
        
        Returns:
            Response -- JSON serialized list of events.
        '''
        print(request.query_params)

        events = []
        if 'game' in request.query_params:
            print('Condition met: Query Params includes "game".')
            if request.query_params['game'] == '1':
                print('Condition met: Query Params includes "game" and value is 1.')
                events = Event.objects.filter(game_id=1)
        else:
            events = Event.objects.all()

        gamer = Gamer.objects.get(user=request.auth.user)

        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        ''' Handles POST operations.
        
        Returns:
            Response -- JSON serialized event instance.
        '''

        gamer = Gamer.objects.get(user=request.auth.user)
        # game = Game.objects.get(pk=request.data['game'])

        event = Event.objects.create(
            description=request.data['description'],
            date=request.data['date'],
            time=request.data['time'],
            game_id=request.data['game'],
            organizer=gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def update(self, request, pk):
        ''' Handles PUT requests for an event.
        
        Returns:
            Response -- Empty body with 204 status code.
        '''

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        gamer = Gamer.objects.get(user=request.auth.user)
        event.organizer = gamer
        game = Game.objects.get(pk=request.data['game'])
        event.game_id = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        ''' Handles DELETE requests for an event. '''

        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['POST'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)


    @action(methods=['DELETE'], detail=True)
    def leave(self, request, pk):
        ''' DELETE request for a user to leave an event. '''

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    ''' JSON serializer for events. '''

    class Meta:
        model = Event
        fields = ('id', 'description', 'game', 'date', 'time', 'attendees', 'organizer', 'joined')
        depth = 2


