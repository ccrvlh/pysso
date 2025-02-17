"""Yandex SSO Login Helper."""

from typing import TYPE_CHECKING, ClassVar, Optional

from litestar_sso.base import DiscoveryDocument, OpenID, SSOBase

if TYPE_CHECKING:
    import httpx  # pragma: no cover


class YandexSSO(SSOBase):
    """Class providing login using Yandex OAuth."""

    provider = "yandex"
    scope: ClassVar = ["login:email", "login:info", "login:avatar"]
    avatar_url = "https://avatars.yandex.net/get-yapic"

    async def get_discovery_document(self) -> DiscoveryDocument:
        """Override the discovery document method to return Yandex OAuth endpoints."""
        return {
            "authorization_endpoint": "https://oauth.yandex.ru/authorize",
            "token_endpoint": "https://oauth.yandex.ru/token",
            "userinfo_endpoint": "https://login.yandex.ru/info",
        }

    async def openid_from_response(self, response: dict, session: Optional["httpx.AsyncClient"] = None) -> OpenID:
        """Converts Yandex user info response to OpenID object."""
        picture = None

        if (avatar_id := response.get("default_avatar_id")) is not None:
            picture = f"{self.avatar_url}/{avatar_id}/islands-200"

        return OpenID(
            email=response.get("default_email"),
            display_name=response.get("display_name"),
            provider=self.provider,
            id=response.get("id"),
            first_name=response.get("first_name"),
            last_name=response.get("last_name"),
            picture=picture,
        )
