"""
This module provides functions to generate OAuth client assertions
and retrieve OAuth tokens for the Apple Business API.

https://developer.apple.com/documentation/apple-school-and-business-manager-api/implementing-oauth-for-the-apple-school-manager-and-apple-business-api
"""

import uuid
from datetime import UTC, datetime

import aiohttp
import jwt


def generate_oauth_client_assertion(
    key_id: str, client_id: str, private_key_pem: str
) -> str:
    headers = {
        "alg": "ES256",
        "kid": key_id,
    }
    iat = int(datetime.now(UTC).timestamp())
    exp = iat + 60 * 5  # Token valid for 5 minutes
    payload = {
        "aud": "https://account.apple.com/auth/oauth2/v2/token",
        "iat": iat,
        "exp": exp,
        "sub": client_id,
        "jti": str(uuid.uuid4()),
        "iss": client_id,
    }
    return jwt.encode(payload, private_key_pem, headers=headers)


async def retrieve_oauth_token(
    key_id: str, client_id: str, private_key_pem: str
) -> dict:
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            "https://account.apple.com/auth/oauth2/token",
            params={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": generate_oauth_client_assertion(
                    key_id, client_id, private_key_pem
                ),
                "scope": "business.api",
            },
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()
