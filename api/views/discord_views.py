import requests
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from discord_perm.discord_perm_const import MANAGE_MESSAGES, ADMINISTRATOR
from discord_perm.discord_perm import has_permission
from kepy.settings.base import CLIENT_ID, CLIENT_SECRET, AUTH_REDIRECT_URL, DISCORD_API
from kepy.discord_api_shortcuts import api_get


def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": AUTH_REDIRECT_URL,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{DISCORD_API}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    return r


@api_view(["POST"])
@permission_classes([AllowAny])
def discord_login(request):
    tokens = exchange_code(request.data.get("code"))
    return HttpResponse(tokens, content_type="application/json", status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_guilds(request):

    bot_guilds = api_get("/users/@me/guilds")
    user_token = request.COOKIES.get("access_token")
    user_guilds = api_get(f"/users/@me/guilds", f"Bearer {user_token}")

    guilds = []

    if bot_guilds and user_guilds:
        for guild in user_guilds:
            if has_permission(int(guild["permissions"]), ADMINISTRATOR):
                user_status = "administrator"
            elif has_permission(int(guild["permissions"]), MANAGE_MESSAGES):
                user_status = "moderator"
            else:
                user_status = "member"

            guild_id, guild_icon = guild["id"], guild["icon"]
            _guild = {
                "id": guild_id,
                "name": guild["name"],
                "user_status": user_status,
                "icon": f"https://cdn.discordapp.com/icons/{guild_id}/{guild_icon}.webp?size=64",
            }
            guilds.append(_guild)

    return Response(guilds, status=200)
