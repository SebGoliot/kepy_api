from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from api.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow members to be viewed and edited
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def retrieve(self, request, guild_pk=None, pk=None):
        member = Member.objects.get(guild=guild_pk, user=pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)
