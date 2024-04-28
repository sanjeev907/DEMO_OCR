from rest_framework.serializers import ModelSerializer
from app.models import *

class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"