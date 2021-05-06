from datetime import datetime, timedelta
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from celery.worker.control import revoke

from api.shortcuts import get_guild_by_id, get_user_by_id
from api.models import Mute
from kepy_worker import app


class MuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mute
        fields = "__all__"


class MuteViewSet(viewsets.ModelViewSet):
    """ Mute API endpoint """

    queryset = Mute.objects.all().order_by("-start_time")
    serializer_class = MuteSerializer

    def retrieve(self, request, guild_pk=None, member_pk=None, pk=None):
        try:
            if guild_pk:
                mute = Mute.objects.get(guild=guild_pk, user=member_pk, pk=pk)
            else:
                mute = Mute.objects.get(user=member_pk, pk=pk)
        except Mute.DoesNotExist:
            return Response(404)

        serializer = MuteSerializer(mute)
        return Response(serializer.data)

    def create(self, request, guild_pk=None, member_pk=None):
        """Creates a mute and prepares the unmute task"""
        reason = request.data.get("reason")
        if not reason:
            author = get_user_by_id(request.data["author"])
            reason = request.data.get("reason", f"muted by {author}")

        guild = get_guild_by_id(guild_pk)
        task_args = (
            guild_pk,
            member_pk,
            guild.mute_role_id,
            reason,
        )
        app.send_task("kepy_worker.mute_worker.mute", task_args)
        unmute_task = app.send_task(
            "kepy_worker.mute_worker.unmute",
            task_args,
            eta=datetime.now() + timedelta(seconds=int(request.data["duration"])),
        )
        request.data._mutable = True
        request.data["guild"] = guild_pk
        request.data["user"] = member_pk
        request.data["unmute_task_id"] = unmute_task.id

        return super().create(request)

    @action(methods=["PUT"], detail=True)
    def cancel(self, request, guild_pk=None, member_pk=None, pk=None):
        """Cancels a mute"""
        if guild_pk:
            mute = Mute.objects.get(guild=guild_pk, user=member_pk, pk=pk)
        else:
            return Response(status=403)
        self.cancel_mute(mute)
        return Response(status=204)

    @staticmethod
    def cancel_mute(mute):
        """Cancels a mute

        Args:
            mute (Mute): The Mute object to cancel
        """
        revoke(state=None, task_id=mute.unmute_task_id)
        mute.revoked = True
        mute.active = False
        mute.save()
