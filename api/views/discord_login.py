import requests
from django.http.response import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


from kepy.settings import CLIENT_ID, CLIENT_SECRET, AUTH_REDIRECT_URL, API_BASE_URL


def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': AUTH_REDIRECT_URL
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(f"{API_BASE_URL}/oauth2/token", data=data, headers=headers)
    print(r.content)
    r.raise_for_status()
    return r


@api_view(['POST'])
@permission_classes([AllowAny])
def discord_login(request):
    code = request.data.get('code')
    r = exchange_code(code)
    return HttpResponse(r, content_type='application/json')
