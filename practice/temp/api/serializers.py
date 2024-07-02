from rest_framework.serializers import ModelSerializer
from temp.models import *


class RoomSerializer(ModelSerializer):
    class Meta:
           model =Rooom
           fields='__all__' 
