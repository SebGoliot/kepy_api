from django.db.models import (
    Model, CharField, IntegerField,
    DateTimeField, SmallIntegerField,
    UniqueConstraint
    )
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey, ManyToManyField


class DiscordUser(Model):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=64)
    discriminator = SmallIntegerField()
    avatar_url = CharField(max_length=1024)
    created_at = DateTimeField()

class Guild(Model):
    id = IntegerField(primary_key=True)
    date_created = DateTimeField(auto_now=True)
    prefix = CharField(max_length=8)
    mute_role_id = IntegerField()

class Member(Model):
    user = ForeignKey(DiscordUser, on_delete=CASCADE)
    guild = ForeignKey(Guild, on_delete=CASCADE)
    joined_at = DateTimeField()
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'guild'], name='unique member'),
        ]    

class Message(Model):
    MESSAGE_STATE = [("DEFAULT", "default"), ("EDITED", "edit"), ("DELETED", "deleted")]
    id = IntegerField(primary_key=True)
    created_at = DateTimeField()
    author = ForeignKey(DiscordUser, on_delete=CASCADE)
    channel_id = IntegerField()
    guild = ForeignKey(Guild, on_delete=CASCADE)
    content = CharField(max_length=2048, default="", blank=True)
    state = CharField(choices=MESSAGE_STATE, default="DEFAULT", max_length=8)
    deleted_at = DateTimeField(auto_now=True, blank=True)
    class Meta:
        ordering = ["created_at"]

class Edit(Model):
    """ Messages edits """
    message = ForeignKey(Message, on_delete=CASCADE)
    content = CharField(max_length=2048, blank=False, default="")
    edit_time = DateTimeField(auto_now=True)

class Attachment(Model):
    """ Attachments associative table """
    message = ForeignKey(Message, on_delete=CASCADE, related_name="message")
    filename = CharField(max_length=1024, default="")
    content_url = CharField(max_length=1024, default="")
    proxy_url = CharField(max_length=1024, default="")

class Mute(Model):
    guild = ForeignKey(Guild, on_delete=CASCADE)
    user = ForeignKey(DiscordUser, on_delete=CASCADE, related_name="muted_user")
    author = ForeignKey(DiscordUser, on_delete=CASCADE, related_name="mute_author")
    duration = IntegerField()
    start_time = DateTimeField(auto_now_add=True)
    active = BooleanField(default=True)
    revoked = BooleanField(default=False)
    unmute_task_id = CharField(max_length=50)
    reason = CharField(max_length=2048, default="", blank=True)
