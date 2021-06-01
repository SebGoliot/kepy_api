from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action

from api.models import Member
from api.helpers.mute import cancel_member_mutes
from api.shortcuts import get_member_by_id


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class MemberViewSet(viewsets.ModelViewSet):
    """API endpoint that allow members to be viewed and edited"""

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def retrieve(self, request, guild_pk=None, pk=None):
        if member := get_member_by_id(guild_pk, pk):
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        return Response(status=404)

    @action(methods=["GET"], detail=True, url_path="cancel-mutes")
    def cancel_mutes(self, request, guild_pk=None, pk=None):
        """Cancels a mute"""
        cancel_member_mutes(guild_pk, pk)
        return Response(status=204)
