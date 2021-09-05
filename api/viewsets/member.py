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

    def retrieve(self, request, guild_pk=None, pk=None) -> Response:
        """Returns a member, creates it if not found

        Args:
            guild_pk (int, optional): The guild ID of the member. Defaults to None.
            pk (int, optional): The member ID. Defaults to None.

        Returns:
            Response: The response containing the member data.
        """
        member = get_member_by_id(guild_pk, pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True, url_path="cancel-mutes")
    def cancel_mutes(self, request, guild_pk=None, pk=None) -> Response:
        """Cancels a member mute

        Args:
            guild_pk (int, optional): The guild ID of the member. Defaults to None.
            pk (int, optional): The member ID. Defaults to None.

        Returns:
            Response: The request response
        """
        cancel_member_mutes(guild_pk, pk)
        return Response(status=204)
