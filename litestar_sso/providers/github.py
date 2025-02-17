"""Github SSO Oauth Helper class."""

from typing import TYPE_CHECKING, ClassVar, Optional

from litestar_sso.base import DiscoveryDocument, OpenID, SSOBase

if TYPE_CHECKING:
    import httpx  # pragma: no cover


class GithubSSO(SSOBase):
    """Class providing login via Github SSO."""

    provider = "github"
    scope: ClassVar = ["user:email"]
    additional_headers: ClassVar = {"accept": "application/json"}
    emails_endpoint = "https://api.github.com/user/emails"

    async def get_discovery_document(self) -> DiscoveryDocument:
        return {
            "authorization_endpoint": "https://github.com/login/oauth/authorize",
            "token_endpoint": "https://github.com/login/oauth/access_token",
            "userinfo_endpoint": "https://api.github.com/user",
        }

    async def _get_primary_email(self, session: Optional["httpx.AsyncClient"] = None) -> Optional[str]:
        """Attempt to get primary email from Github for a current user.
        The session received must be authenticated.
        """
        if not session:
            return None
        response = await session.get(self.emails_endpoint)
        if response.status_code != 200:
            return None
        emails = response.json()
        for email in emails:
            if email["primary"]:
                return email["email"]
        return None

    async def openid_from_response(self, response: dict, session: Optional["httpx.AsyncClient"] = None) -> OpenID:
        return OpenID(
            email=response.get("email") or (await self._get_primary_email(session)),
            provider=self.provider,
            id=str(response["id"]),
            display_name=response["login"],
            picture=response["avatar_url"],
        )
