from rest_framework import serializers
from .models import Todo, UserRole
from django.contrib.auth.models import User
from django.utils.timezone import now

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only = True)
    role = serializers.ChoiceField(choices = UserRole.choices, default = 'user')
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username= validated_data['username'],
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
            password= validated_data['password']
        )
        user.profile.role = role
        return user 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
      
    
class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank = True)
    completed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        return Todo.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        if validated_data.get('completed'):
            instance.completed = True
            instance.completed_at = now()

        instance.save()
        return instance

# class TodoSerilaizer(serializers.ModelSerializer):
#     class Meta:
#         model = Todo
#         fields = ['id','title', 'description','completed', 'created_at']
#         read_only_fields = ['id', 'created_at']

# class EmployeeSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=50)
#     description = serializers.CharField(allow_blank = True, required = False)
#     department = serializers.CharField(max_length=50)
    
#     def create(self, validated_data):
#         return Employee.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.description = validated_data.get('description', instance.description)
#         instance.department = validated_data.get('department', instance.department)
#         instance.save()
#         return instance 