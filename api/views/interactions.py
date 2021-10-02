from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from discord_perm.discord_perm_const import MANAGE_MESSAGES
from discord_perm.discord_perm import has_permission

from api.helpers.interactions import (
    get_interaction_author_id,
    get_interaction_author_permissions,
    get_interaction_guild_id,
    get_interaction_name,
)
from api.helpers.app_interactions import get_app_message_author
from api.helpers.mute import create_mute


@api_view(["POST"])
@permission_classes([AllowAny])
def interactions(request):

    PING                = "1"
    APPLICATION_COMMAND = "2"
    MESSAGE_COMPONENT   = "3"

    verify_key = VerifyKey(bytes.fromhex(settings.KEPY_PUBLIC_KEY))
    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return HttpResponse("invalid request signature", status=401)

    interaction_type = str(request.data.get("type"))

    if interaction_type == PING:
        return JsonResponse(data={"type": 1})
    elif interaction_type == APPLICATION_COMMAND:
        if int_name := get_interaction_name(body):
            if interact := interact_bindings.get(int_name):
                response = interact(body)
                return JsonResponse(data={"content": response})

    return HttpResponseBadRequest()


def mute_author(body) -> str:
    """This function handles the mute app interaction and returns a message

    Args:
        body (dict): The interaction request body

    Returns:
        str: The returned message
    """

    if has_permission(get_interaction_author_permissions(body), MANAGE_MESSAGES):
        muted = get_app_message_author(body)
        create_mute(
            guild_id=get_interaction_guild_id(body),
            author_id=get_interaction_author_id(body),
            muted_id=muted["id"],
            duration=30 * 60,
            reason="Muted with application command",
        )
        return _mute_success(muted["username"], 30, True)
    return _mute_success("", 30, False)


def _mute_success(muted_name: str, duration: int, success: bool):
    if success:
        return f"{muted_name} has been muted for {duration} minutes."
    return "Seems like you are not allowed to do this.."


interact_bindings = {"Mute author": mute_author}
