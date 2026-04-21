from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import *

class RegisterView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Registered'})
        return Response(serializer.errors, status= 400)
    
class LoginView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data= request.data)
        
        if serializer.is_valid():
            user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
            )
        
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response({'error': 'Invalid Credentials'}, status=401)
        
        return Response(serializer.errors, status=400)
# # Create your views here.
# def api_root(request):
#     """API root endpoint showing available endpoints"""
#     return JsonResponse({
#         'message': 'Todo API',
#         'endpoints': {
#             'todos': '/api/todos/',
#             'todo_detail': '/api/todos/<int:pk>/',
#             'employees': '/api/employees/',
#         },
#         'methods': {
#             'todos': 'GET, POST',
#             'todo_detail': 'GET, PUT, DELETE',
#             'employees': 'GET, POST'
#         }
#     })


class TodoListCreateView(APIView):
    permission_classes = [IsUser]
    
    def get(self, request):
        
        todos = Todo.objects.all()
        if not todos.exists():
            return Response(
                {'Message': 'Todos Not Found'}, status= status.HTTP_404_NOT_FOUND
            )
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        role = request.user.profile.role

        if role == 'superadmin':
            todos = Todo.objects.all()

        elif role == 'admin':
            todos = Todo.objects.all()

        elif role == 'manager':
            todos = Todo.objects.filter(user__profile__role='user')

        else:  # normal user
            todos = Todo.objects.filter(user=request.user)

        if not todos.exists:
            return Response(
                {'Message': 'Todos Not Found'}, status= status.HTTP_404_NOT_FOUND
            )
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = TodoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListView(APIView):
    permission_classes = [IsUser]
    
    def get_object(self, pk, user):
        try:
            return Todo.objects.get(pk=pk, user=user)
        except Todo.DoesNotExist:
            return None
    
    def has_access(self, request, todo):
        role = request.user.profile.role

        if role in ['superadmin', 'admin']:
            return True
        elif role == 'manager':
            return todo.user.profile.role == 'user'
        else:
            return todo.user == request.user
    
    def get(self, request, pk):
        todo =self.get_object(pk, request.user)
        if not todo or not self.has_access(request, todo):
            return Response({'error': 'Forbidden'}, status=404)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    def put(self, request,pk):
        todo = self.get_object(pk, request.user)
        if not todo or not self.has_access(request, todo):
            return Response({'error': 'Forbidden'}, status = 404)
        serializer = TodoSerializer(todo, data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    
    def delete(self,request,pk):
        todo = self.get_object(pk, request.user)
        if not todo or not self.has_access(request, todo):
            return Response({'error': 'Forbidden'}, status = 403)
        todo.delete()
        return Response({'message' : 'Deleted Successfully '}, status= 204)
    


# class EmployeeListCreateView(APIView):
#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many = True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
# class EmployeeListView(APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return None
    
#     def get(self, request, pk):
#         employee = self.get_object(pk =pk)
#         if not employee:
#             return Response({'error':'Not Found'}, status=404)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         employee = self.get_object(pk=pk)
#         if not employee:
#             return Response({'error':'Not Found'}, status=404)
#         serializer = EmployeeSerializer(employee, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status = 400)
    
#     def delete(self, request, pk):
#         employee = self.get_object(pk=pk)
#         if not employee:
#             return Response({'error': 'Not Found'}, status = 404)        
#         employee.delete()
#         return Response({'message' : 'Deleted Successfully '}, status= 204)