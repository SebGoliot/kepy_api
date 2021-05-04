from django.urls import include, path

from api.views.discord_user import DiscordUserViewSet
from api.views.guild import GuildViewSet
from api.views.member import MemberViewSet
from api.views.message import MessageViewSet
from api.views.mute import MuteViewSet
from rest_framework_nested import routers

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

users_router.register("messages", MuteViewSet, basename="user-messages")
# /users/{user_pk}/messages
# /users/{user_pk}/messages/{message_pk}

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


# router.register('messages', views.MessageViewSet)
# router.register('attachments', views.AttachmentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("", include(users_router.urls)),
    path("", include(guilds_router.urls)),
    path("", include(members_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]


# router.register('members', views.MemberViewSet)
