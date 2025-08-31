from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ToDoSerializer,TodoToggleCompleteSerializer
from todo.models import ToDo
from django.db import IntegrityError 
from django.contrib.auth.models import User 
from rest_framework.parsers import JSONParser 
from rest_framework.authtoken.models import Token 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods


class TodoListCreate(generics.ListCreateAPIView): 
# ListAPIView requires two mandatory attributes, serializer_class and 
# queryset. 
# We specify TodoSerializer which we have earlier implemented 
    serializer_class = ToDoSerializer 
    permission_classes = [permissions.IsAuthenticated] 


    def get_queryset(self): 
        user = self.request.user 
        return ToDo.objects.filter(user=user).order_by('-created')
    
    def perform_create(self, serializer): 
        # serializer holds a django model 
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = ToDoSerializer 
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self): 
        user = self.request.user 
        # user can only update, delete own posts 
        return ToDo.objects.filter(user=user)
    
class TodoToggleComplete(generics.UpdateAPIView): 
    serializer_class = TodoToggleCompleteSerializer 
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self): 
        user = self.request.user 
        return ToDo.objects.filter(user=user) 

    def perform_update(self,serializer): 
        serializer.instance.completed=not(serializer.instance.completed) 
        serializer.save()

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data = JSONParser().parse(request)  # dict con 'username' y 'password'
        user = User.objects.create_user(
            username=data['username'],
            password=data['password']
        )
        user.save()
        token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=201)
    except IntegrityError:
        return JsonResponse({'error': 'username ya existe, elige otro'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'faltan campos: username y password'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    data = JSONParser().parse(request)
    user = authenticate(
        request,
        username=data.get('username'),
        password=data.get('password')
    )
    if user is None:
        return JsonResponse({'error': 'no se pudo iniciar sesión: revisa usuario/clave'}, status=400)

    # devolver token (crearlo si no existe)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': str(token)}, status=201)