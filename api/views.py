from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from api.serializers import *
from api.models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow users to be viewed and edited
    """
    queryset = DiscordUser.objects.all().order_by('id')
    serializer_class = UserSerializer

class GuildViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow guilds to be viewed or edited
    """
    queryset = Guild.objects.all().order_by('-date_created')
    serializer_class = GuildSerializer

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow members to be viewed and edited
    """
    queryset = Member.objects.all().order_by('id')
    serializer_class = MemberSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow messages to be viewed and edited
    """
    queryset = Message.objects.all().order_by('id')
    serializer_class = MessageSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow attachments to be viewed and edited
    """
    queryset = Attachment.objects.all().order_by('id')
    serializer_class = AttachmentSerializer
