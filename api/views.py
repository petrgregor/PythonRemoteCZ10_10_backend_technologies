from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.parsers import JSONParser

from chatterapp.models import *

from api.serializers import *

# Create your views here.
#class RoomsApiView(APIView):
#    permission_classes = [permissions.IsAuthenticated]  # pouze pro přihlášené uživatele

#@api_view(['GET'])
def hello_world(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello, world!",
                             "api": "REST api",
                             "method": "GET"})
    elif request.method == 'POST':
        return JsonResponse({"message": "Hello, world!",
                             "method": "POST"})

# získáme seznam všech místností
def rooms(request):
    # pokud metoda GET -> vrátíme seznam všech místností
    if request.method == 'GET':
        rooms = Room.objects.all()  # z dabáze vytáhneme všechny záznamy
        serializer = RoomSerializer(rooms, many=True)  # many=True, protože nám vrátí více výsledků
        return JsonResponse(serializer.data, safe=False)
    # pokud metoda POST -> vytvoříme novou místnost
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


# získáme informace o jedné místnosti
def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return HttpResponse(status=404)
    # pokud metoda GET -> získáme informace o místnosti
    if request.method == 'GET':
        serializer = RoomSerializer(room, many=False)  # many=False, protože nám vrátí jeden výsledek
        return JsonResponse(serializer.data, safe=False)
    # pokud metoda PUT -> editujeme informace o místnosti
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(room, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    # pokud metoda DELETE -> mažeme místnost
    elif request.method == 'DELETE':
        room.delete()
        return HttpResponse(status=204)

# chceme získat všechny zprávy ze zadané místnosti
def messages(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)  # všechny zprávy z dané místnosti
    serializer = MessageSerializer(messages, many=True)
    return JsonResponse(serializer.data, safe=False)
