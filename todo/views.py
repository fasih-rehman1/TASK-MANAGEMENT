from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class TodoListCreateView(APIView):
    
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoListView(APIView):
    
    def get_object(self, pk):
        try:
            return Todo.objects.get(id=pk)
        except Todo.DoesNotExist:
            return None
    
    def get(self, request, pk):
        todo =self.get_object(pk)
        if not todo:
            return Response({'error': 'Not found'}, status=404)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    def put(self, request,pk):
        todo = self.get_object(pk)
        if not todo:
            return Response({'error': 'Not found'}, status = 404)
        serializer = TodoSerializer(todo, data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    
    def delete(self,request,pk):
        todo = self.get_object(pk)
        if not todo:
            return Response({'error': 'Not found'}, status = 404)
        todo.delete()
        return Response({'message' : 'Deleted Successfully '}, status= 204)