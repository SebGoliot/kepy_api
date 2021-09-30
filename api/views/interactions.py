from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


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
        pass
    elif interaction_type == MESSAGE_COMPONENT:
        pass

    return HttpResponseBadRequest()
