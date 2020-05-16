from rest_framework import serializers
from .models import Task, MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email',)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()


class TaskFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'execution_date', 'is_executed')

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'execution_date')


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    name = serializers.CharField(required=True)
    execution_date = serializers.DateField()
    created_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        task = Task(**validated_data)
        current_user = MyUser.objects.get(is_logged=True)
        task.created_by = current_user
        current_user.logged(False)
        current_user.save()
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.execution_date = validated_data.get('execution_date', instance.execution_date)

        instance.save()
        return instance


class ExecuteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    name = serializers.CharField(required=True)
    execution_date = serializers.DateField()
    created_by = UserSerializer(read_only=True)
    is_executed = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.is_executed = validated_data.get('is_executed', instance.is_executed)

        instance.save()
        return instance


