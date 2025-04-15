# app/platform/jose_utils.py
import requests
from jose import jwt
from jose.utils import base64url_decode
from jose import jwk
from app.foundation.settings import GOOGLE_CLIENT_ID

GOOGLE_JWK_URL = "https://www.googleapis.com/oauth2/v3/certs"

_jwk_cache = {}  # 캐시 메모리 (선택적으로 활용 가능)


def get_public_key(token: str):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")

    if kid in _jwk_cache:
        return _jwk_cache[kid]

    jwks = requests.get(GOOGLE_JWK_URL).json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            _jwk_cache[kid] = key
            return key

    return None


async def decode_jwt(token: str):
    try:
        key = get_public_key(token)
        if key is None:
            return None

        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=GOOGLE_CLIENT_ID,
            issuer="https://accounts.google.com"
        )

    except Exception:
        return None
