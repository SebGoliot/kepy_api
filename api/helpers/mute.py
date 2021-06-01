
from celery.worker.control import revoke
from api.models import Mute

def cancel_mute(mute):
    """Cancels a mute

    Args:
        mute (Mute): The Mute object to cancel
    """
    revoke(state=None, task_id=mute.unmute_task_id)
    mute.revoked = True
    mute.active = False
    mute.save()

def cancel_member_mutes(guild_id, user_id):
    mutes = Mute.objects.filter(guild=guild_id, user=user_id, active=True)
    for mute in mutes:
        cancel_mute(mute)

def end_member_mutes(guild_id, user_id):
    mutes = Mute.objects.filter(guild=guild_id, user=user_id, active=True)
    for mute in mutes:
        mute.active = False
        mute.save()
