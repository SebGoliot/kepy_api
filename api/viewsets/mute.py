from datetime import datetime, timedelta
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Guild, Member, Mute

from kepy_worker import app
from celery.worker.control import revoke

class MuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mute
        fields = "__all__"


class MuteViewSet(viewsets.ModelViewSet):
    """ Mute API endpoint """

    queryset = Mute.objects.all().order_by("id")
    serializer_class = MuteSerializer

    def create(self, request):
        member = request.data['member']
        guild = Guild.objects.get(pk=member.guild.id)
        user_id = member.user.id
        author = Member.objects.get(pk=request.data['author'])

        app.send_task(
            'kepy_worker.mute_worker.mute',
            (
                guild.id,
                member.user.id,
                guild.mute_role_id,
                request.data['duration'],
                request.data['author'],
                request.data['reason']
            )
        )

        unmute_task = app.send_task(
            'kepy_worker.mute_worker.unmute',
            (
                guild.id,
                member.user.id,
                guild.mute_role_id,
                request.data['reason']
            ),
            eta=datetime.now() + timedelta(seconds=request.data['duration'])
        )

        request.data['unmute_task_id'] = unmute_task.id
        super().create(request)
        return Response(status=204)

    @action(methods=["PUT"], detail=True)
    def cancel(self, request, pk=None):
        """Cancels a mute"""
        mute_obj = self.get_object()

        revoke(state=None, task_id=mute_obj.unmute_task_id)
        mute_obj.revoked = True
        mute_obj.active = False
        mute_obj.save()
        # serializer = self.get_serializer(mute_obj, many=False)
        # return Response(serializer.data)
        return Response(status=204)
