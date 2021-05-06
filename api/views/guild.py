from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

from api.models import Guild
from api.shortcuts import get_guild_by_id


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"


class GuildViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow guilds to be viewed or edited
    """

    queryset = Guild.objects.all().order_by("-date_created")
    serializer_class = GuildSerializer

    def retrieve(self, request, pk=None):
        if guild := get_guild_by_id(pk):
            serializer = GuildSerializer(get_guild_by_id(pk))
            return Response(serializer.data)
        return Response(status=404)
