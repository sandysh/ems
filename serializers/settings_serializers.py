from rest_framework import serializers
from settings.models import Settings


class SettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Settings
        fields='__all__'