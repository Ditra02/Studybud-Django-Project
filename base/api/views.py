from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# this shows us all the routes in our api
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',      # home of api
        'GET /api/rooms', # lets say we create api to people to see all the rooms in our app
        'GET /api/rooms/:id'
    ]
    return Response(routes) 
    # safe means that we can use python dict inside of this response
    # safe gonna allow routes list to be turned into a json list
    # so that jsonresponse gonna convert this data into json 

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # many = allow multiple objects to be serialize, if false then just one 
        
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)

    return Response(serializer.data)