from rest_framework import viewsets
from rest_framework import serializers

from api.models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"


class AttachmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow attachments to be viewed and edited
    """

    queryset = Attachment.objects.all().order_by("id")
    serializer_class = AttachmentSerializer
