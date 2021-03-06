from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DateTimeField,
    BigIntegerField,
    UniqueConstraint,
)
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey


class DiscordUser(Model):
    id = BigIntegerField(primary_key=True)


class Guild(Model):
    id = BigIntegerField(primary_key=True)
    date_created = DateTimeField()
    prefix = CharField(max_length=8, default="%")
    mute_role_id = BigIntegerField(default=0)


class Member(Model):
    user = ForeignKey(DiscordUser, on_delete=CASCADE)
    guild = ForeignKey(Guild, on_delete=CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "guild"], name="unique member"),
        ]


class Message(Model):
    MESSAGE_STATE = [("DEFAULT", "default"), ("EDITED", "edit"), ("DELETED", "deleted")]
    id = BigIntegerField(primary_key=True)
    created_at = DateTimeField()
    author = ForeignKey(DiscordUser, on_delete=CASCADE)
    channel_id = BigIntegerField()
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
