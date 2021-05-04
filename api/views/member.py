from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from celery.worker.control import revoke

from api.models import Member, Mute


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

    @action(methods=["PUT"], detail=True, url_path="cancel-mutes")
    def cancel_mutes(self, request, guild_pk=None, pk=None):
        """Cancels a mute"""

        mutes = Mute.objects.filter(guild=guild_pk, user=pk)

        for mute in mutes:
            revoke(state=None, task_id=mute.unmute_task_id)
            mute.revoked = True
            mute.active = False
            mute.save()

        return Response(status=204)
