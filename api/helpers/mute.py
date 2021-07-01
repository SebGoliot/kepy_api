from api.shortcuts import get_guild_by_id
from celery.worker.control import revoke
from api.models import Mute
from kepy_worker import app


def cancel_mute(mute, reason: str = ""):
    """Cancels a mute

    Args:
        mute (Mute): The Mute object to cancel
        reason (str): The reason why the mute has been canceled
    """
    revoke(state=None, task_id=mute.unmute_task_id)
    guild_id = mute.guild.id
    member_id = mute.user.id
    mute_role_id = get_guild_by_id(guild_id).mute_role_id
    task_args = (guild_id, member_id, mute_role_id, reason)
    app.send_task("kepy_worker.mute_tasks.tasks.unmute", task_args)
    mute.revoked = True
    mute.active = False
    mute.save()


def cancel_member_mutes(guild_id, user_id):
    """Cancels a member's mutes

    Args:
        guild_id (int): The guild id
        user_id (int): The member's user id
    """
    mutes = Mute.objects.filter(guild=guild_id, user=user_id, active=True)
    for mute in mutes:
        cancel_mute(mute)


def end_member_mutes(guild_id, user_id):
    """End a member's mute

    Args:
        guild_id (int): The guild id
        user_id (int): The member's user id
    """
    mutes = Mute.objects.filter(guild=guild_id, user=user_id, active=True)
    for mute in mutes:
        mute.active = False
        mute.save()
