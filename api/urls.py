from rest_framework_nested import routers
from django.urls import include, path

from api.viewsets.discord_user import DiscordUserViewSet
from api.viewsets.guild import GuildViewSet
from api.viewsets.member import MemberViewSet
from api.viewsets.message import MessageViewSet
from api.viewsets.mute import MuteViewSet
from api.views.discord_views import get_user_guilds, discord_login

router = routers.DefaultRouter()

router.register("users", DiscordUserViewSet)
# /users/
# /users/{pk}/
router.register("guilds", GuildViewSet)
# /guilds/
# /guilds/{pk}/

users_router = routers.NestedSimpleRouter(router, "users", lookup="member")
users_router.register("mutes", MuteViewSet, basename="user-mutes")
# /users/{user_pk}/mutes
# /users/{user_pk}/mutes/{mute_pk}

users_router.register("messages", MessageViewSet, basename="user-messages")
# /users/{user_pk}/messages
# /users/{user_pk}/messages/{message_pk}

users_router.register("guilds", GuildViewSet, basename="user-guilds")
# /users/{user_pk}/guilds
# /users/{user_pk}/guilds/{guild_pk}

guilds_router = routers.NestedSimpleRouter(router, "guilds", lookup="guild")
guilds_router.register("members", MemberViewSet, basename="guild-members")
# /guilds/{guild_pk}/members/
# /guilds/{guild_pk}/members/{member_pk}/

guilds_router.register("messages", MessageViewSet, basename="guild-messages")
# /guilds/{guild_pk}/messages/
# /guilds/{guild_pk}/messages/{message_pk}/

members_router = routers.NestedSimpleRouter(guilds_router, "members", lookup="member")
members_router.register("mutes", MuteViewSet, basename="member-mutes")
# /guilds/{guild_pk}/members/{member_pk}/mutes
# /guilds/{guild_pk}/members/{member_pk}/mutes/{mute_pk}


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("login/", discord_login, name="discord_login"),
    path("user-guilds/", get_user_guilds, name="get_user_guilds"),
    path("", include(router.urls)),
    path("", include(users_router.urls)),
    path("", include(guilds_router.urls)),
    path("", include(members_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]


# router.register('members', views.MemberViewSet)
