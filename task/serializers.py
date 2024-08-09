from project.models import Project, Status, Task
from django.contrib.auth.models import User
from project.serializers import ProjectSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'id': {'read_only': True}}


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']
        extra_kwargs = {'id': {'read_only': True}}


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    attachment_urls = serializers.SerializerMethodField()
    status = StatusSerializer(read_only=True)
    start_time = serializers.DateTimeField(format="%d/%b/%Y")
    end_time = serializers.DateTimeField(format="%d/%b/%Y")

    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'owner', 'start_time', 'end_time', 'assigned_to',
                  'attachment_urls', 'start_time', 'end_time']
        extra_kwargs = {'id': {'read_only': True}}

    def get_attachment_urls(self, obj):
        return [f'/media/{attachment}' for attachment in obj.attachments]
