from api.models import Attachment, DiscordUser, Guild, Member, Message
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = '__all__'

class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
