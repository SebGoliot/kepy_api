from rest_framework import viewsets
from rest_framework import serializers

from api.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow messages to be viewed and edited
    """

    queryset = Message.objects.all().order_by("id")
    serializer_class = MessageSerializer
