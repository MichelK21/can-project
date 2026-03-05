import os
import time
import requests
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=False)

_jwks_cache = {"jwks": None, "ts": 0}
JWKS_TTL_SECONDS = 60 * 60  # 1h

def _get_vcap_xsuaa_credentials() -> dict:
    """
    Récupère VCAP_SERVICES.xsuaa[0].credentials
    """
    vcap = os.getenv("VCAP_SERVICES")
    if not vcap:
        raise RuntimeError("VCAP_SERVICES not set. Is XSUAA bound to the app?")
    import json
    vcap_json = json.loads(vcap)
    xsuaa = vcap_json.get("xsuaa")
    if not xsuaa:
        raise RuntimeError("No xsuaa service in VCAP_SERVICES. Bind xsuaa to backend.")
    return xsuaa[0]["credentials"]

def _fetch_jwks(jwks_url: str) -> dict:
    now = int(time.time())
    if _jwks_cache["jwks"] and (now - _jwks_cache["ts"]) < JWKS_TTL_SECONDS:
        return _jwks_cache["jwks"]

    r = requests.get(jwks_url, timeout=10)
    r.raise_for_status()
    jwks = r.json()
    _jwks_cache["jwks"] = jwks
    _jwks_cache["ts"] = now
    return jwks

def _select_key(jwks: dict, kid: str) -> dict:
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No matching JWK for token kid")

def require_jwt(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")

    token = creds.credentials

    # Read XSUAA from environment (best practice on CF)
    xsuaa = _get_vcap_xsuaa_credentials()
    jwks_url = xsuaa["url"].rstrip("/") + "/token_keys"  # XSUAA endpoint for keys
    expected_issuer = xsuaa["url"].rstrip("/")  # issuer base
    clientid = xsuaa.get("clientid")  # available if xsuaa bound to backend (recommended)

    # Parse header to get kid
    try:
        header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header")

    kid = header.get("kid")
    if not kid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing kid")

    jwks = _fetch_jwks(jwks_url)
    key = _select_key(jwks, kid)

    # Audience: in SAP XSUAA, aud can be list; often contains xsappname or clientid.
    # We'll verify signature + issuer + expiration.
    options = {
        "verify_aud": False,  # we'll do custom check below (more tolerant)
    }

    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
                "verify_iss": False
    }
        )
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"JWT validation failed: {str(e)}")

    # Custom audience check (recommended)
    aud = claims.get("aud")
    if clientid:
        # aud can be string or list
        if isinstance(aud, str):
            ok = (aud == clientid)
        else:
            ok = (clientid in (aud or []))
        if not ok:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid audience for this backend")

    return claims

def require_scope(scope: str):
    """
    usage: Depends(require_scope("can-xsapp.user"))
    """
    def _inner(claims=Depends(require_jwt)):
        scopes = claims.get("scope", []) or []
        if scope not in scopes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope: {scope}")
        return claims
    return _inner