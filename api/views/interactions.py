from django.http.response import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes([AllowAny])
def interactions(request):
    if request.data.get("type") == "1":  # If the interaction is a PING
        return JsonResponse(data={"type": 1})
    
    return HttpResponseBadRequest()
