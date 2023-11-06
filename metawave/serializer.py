from rest_framework.serializers import ModelSerializer
from .models import MusicList

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = MusicList
        fields = '__all__'
        