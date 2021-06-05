from rest_framework import viewsets
from rest_framework import serializers

from api.models import DiscordUser


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = "__all__"


class DiscordUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow users to be viewed and edited
    """

    queryset = DiscordUser.objects.all().order_by("id")
    serializer_class = DiscordUserSerializer
