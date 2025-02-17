"""Microsoft Login Example"""

import os

import uvicorn
from litestar import Litestar, Request, get

from litestar_sso.providers.microsoft import MicrosoftSSO

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
TENANT = os.environ["TENANT"]

app = Litestar()

sso = MicrosoftSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    tenant=TENANT,
    redirect_uri="http://localhost:8080/auth/callback",
    allow_insecure_http=True,
)


@get("/auth/login")
async def auth_init():
    """Initialize auth and redirect"""
    async with sso:
        return await sso.get_login_redirect()


@get("/auth/callback")
async def auth_callback(request: Request):
    """Verify login"""
    async with sso:
        return await sso.verify_and_process(request)


if __name__ == "__main__":
    uvicorn.run(app="examples.microsoft:app", host="127.0.0.1", port=8080)
