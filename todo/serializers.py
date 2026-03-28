from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank = True)
    completed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
 
# class TodoSerilaizer(serializers.ModelSerializer):
#     class Meta:
#         model = Todo
#         fields = ['id','title', 'description','completed', 'created_at']
#         read_only_fields = ['id', 'created_at']