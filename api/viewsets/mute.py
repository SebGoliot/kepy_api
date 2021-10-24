from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Mute
from api.helpers.mute import cancel_mute, create_mute


class MuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mute
        fields = "__all__"


class MuteViewSet(viewsets.ModelViewSet):
    """ Mute API endpoint """

    queryset = Mute.objects.all().order_by("-start_time")
    serializer_class = MuteSerializer

    def retrieve(self, request, guild_pk=None, member_pk=None, pk=None) -> Response:
        try:
            if guild_pk:
                mute = Mute.objects.get(guild=guild_pk, user=member_pk, pk=pk)
            else:
                mute = Mute.objects.get(user=member_pk, pk=pk)
        except Mute.DoesNotExist:
            return Response(status=404)

        serializer = MuteSerializer(mute)
        return Response(serializer.data)

    def create(self, request, guild_pk=None, member_pk=None) -> Response:
        """Creates a mute and prepares the unmute task"""

        mute = create_mute(
            guild_id = guild_pk,
            author_id = request.data["author"],
            muted_id = member_pk,
            duration = request.data["duration"],
            reason = request.data.get("reason"),
            )

        serializer = MuteSerializer(mute)
        return Response(serializer.data, status=201)


    @action(methods=["PUT"], detail=True)
    def cancel(self, request, guild_pk=None, member_pk=None, pk=None) -> Response:
        """Cancels a mute"""
        if guild_pk:
            mute = Mute.objects.get(guild=guild_pk, user=member_pk, pk=pk)
            cancel_mute(mute)
            return Response(status=204)
        else:
            return Response(status=403)