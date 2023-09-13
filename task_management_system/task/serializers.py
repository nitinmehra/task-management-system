from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    mode = 'add'

    def __init__(self, instance=None, data=..., **kwargs):
        super(TaskSerializer, self).__init__(instance, data, **kwargs)
        # self.Meta.fields = list(self.Meta.fields)
        # setting the mode: add/update, using mode for various purpose like adding validation based on mode or adding/updating fields based on mode
        self.mode = self.context.get('mode')

    def validate(self, attrs):
        
        return attrs


    # create task
    def create(self, validated_data):
        res =  Task.objects.create(**validated_data)
        return res
    
    # update task
    def update(self, instance, validated_data):
        res = super().update(instance, validated_data)
        return res
    


class TaskResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"