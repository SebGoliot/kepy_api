from rest_framework import viewsets
from rest_framework import serializers

from api.models import Guild



class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = '__all__'



class GuildViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow guilds to be viewed or edited
    """

    queryset = Guild.objects.all().order_by("-date_created")
    serializer_class = GuildSerializer

