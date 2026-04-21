from django.urls import path
from .views import *

urlpatterns = [
    # path('', api_root, name='api-root'),  
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('todos/', TodoListCreateView.as_view()),
    path('todos/<int:pk>/', TodoListView.as_view()),
    
    # path('employees/', EmployeeListCreateView.as_view(), name='employee-list'),
    # path('employees/<int:pk>/', EmployeeListView.as_view(), name='employee-detail'), 
]
    
