from django.urls import path
from .views import *

urlpatterns = [
    path('todos/', TodoListCreateView.as_view()),
    path('todos/<int:pk>/', TodoListView.as_view()),
]