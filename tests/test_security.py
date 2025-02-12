import unittest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
import jwt

from app.security import (
    _get_jwt_payload,
    _verify_token_type,
    verify_access_token,
    verify_refresh_token,
    _create_jwt_token,
    create_access_token,
    create_refresh_token,
    _get_user_id_from_token,
    set_current_user_id,
    get_current_user_id,
)
from app.models.user import Users
from app.config import jwt_settings


class TestSecurity(unittest.IsolatedAsyncioTestCase):

    @patch("app.security.jwt.decode")
    async def test_get_jwt_payload_valid(self, mock_decode):
        mock_decode.return_value = {"sub": "1", "type": "access"}
        token = "valid.token.here"
        payload = await _get_jwt_payload(token)
        self.assertEqual(payload, {"sub": "1", "type": "access"})

    @patch("app.security.jwt.decode", side_effect=jwt.PyJWTError("Invalid token"))
    async def test_get_jwt_payload_invalid(self, mock_decode):
        token = "invalid.token.here"
        with self.assertRaises(HTTPException):
            await _get_jwt_payload(token)

    @patch("app.security._get_jwt_payload", new_callable=AsyncMock)
    async def test_verify_token_type_valid(self, mock_get_jwt_payload):
        mock_get_jwt_payload.return_value = {"sub": "1", "type": "access"}
        credentials = AsyncMock(credentials="valid.token.here")
        sub = await _verify_token_type(credentials, "access")
        self.assertEqual(sub, "1")

    @patch("app.security._get_jwt_payload", new_callable=AsyncMock)
    async def test_verify_token_type_invalid(self, mock_get_jwt_payload):
        mock_get_jwt_payload.return_value = {"sub": "1", "type": "refresh"}
        credentials = AsyncMock(credentials="valid.token.here")
        with self.assertRaises(HTTPException):
            await _verify_token_type(credentials, "access")

    @patch("app.security._verify_token_type", new_callable=AsyncMock)
    async def test_verify_access_token(self, mock_verify_token_type):
        mock_verify_token_type.return_value = "1"
        credentials = AsyncMock(credentials="valid.token.here")
        sub = await verify_access_token(credentials)
        self.assertEqual(sub, "1")

    @patch("app.security._verify_token_type", new_callable=AsyncMock)
    async def test_verify_refresh_token(self, mock_verify_token_type):
        mock_verify_token_type.return_value = "1"
        credentials = AsyncMock(credentials="valid.token.here")
        sub = await verify_refresh_token(credentials)
        self.assertEqual(sub, "1")

    def test_create_jwt_token_access(self):
        user = Users(id=1, email="test@example.com")
        token = _create_jwt_token(user, "access")
        payload = jwt.decode(
            token,
            jwt_settings.authjwt_secret_key,
            algorithms=[jwt_settings.authjwt_algorithm],
        )
        self.assertEqual(payload["sub"], "1")
        self.assertEqual(payload["type"], "access")

    def test_create_jwt_token_refresh(self):
        user = Users(id=1, email="test@example.com")
        token = _create_jwt_token(user, "refresh")
        payload = jwt.decode(
            token,
            jwt_settings.authjwt_secret_key,
            algorithms=[jwt_settings.authjwt_algorithm],
        )
        self.assertEqual(payload["sub"], "1")
        self.assertEqual(payload["type"], "refresh")

    @patch("app.security._create_jwt_token")
    async def test_create_access_token(self, mock_create_jwt_token):
        mock_create_jwt_token.return_value = "access.token.here"
        user = Users(id=1, email="test@example.com")
        token = await create_access_token(user)
        self.assertEqual(token, "access.token.here")

    @patch("app.security._create_jwt_token")
    async def test_create_refresh_token(self, mock_create_jwt_token):
        mock_create_jwt_token.return_value = "refresh.token.here"
        user = Users(id=1, email="test@example.com")
        token = await create_refresh_token(user)
        self.assertEqual(token, "refresh.token.here")

    @patch("app.security._get_jwt_payload", new_callable=AsyncMock)
    async def test_get_user_id_from_token(self, mock_get_jwt_payload):
        mock_get_jwt_payload.return_value = {"sub": "1"}
        token = "valid.token.here"
        user_id = await _get_user_id_from_token(token)
        self.assertEqual(user_id, 1)

    @patch("app.security._get_user_id_from_token", new_callable=AsyncMock)
    async def test_set_current_user_id(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = 1
        token = "valid.token.here"
        await set_current_user_id(token)
        self.assertEqual(get_current_user_id(), 1)

    @patch("app.security._get_user_id_from_token", new_callable=AsyncMock)
    async def test_set_current_user_id_invalid(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.side_effect = Exception("Invalid token")
        token = "invalid.token.here"
        await set_current_user_id(token)
        self.assertIsNone(get_current_user_id())


if __name__ == "__main__":
    unittest.main()
