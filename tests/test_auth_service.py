from datetime import timedelta

from jose import jwt

from src.config.settings import settings
from src.services.auth_service import AuthService


def make_service():
    # Password hashing and token creation do not touch the database.
    return AuthService(db=None)


def test_password_hash_roundtrip():
    service = make_service()
    hashed = service.get_password_hash("s3cret-pass")
    assert hashed != "s3cret-pass"
    assert service.verify_password("s3cret-pass", hashed)
    assert not service.verify_password("wrong-pass", hashed)


def test_access_token_contains_subject_and_expiry():
    service = make_service()
    token = service.create_access_token({"sub": "alice"})
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_access_token_respects_custom_expiry():
    service = make_service()
    short = service.create_access_token({"sub": "a"}, timedelta(minutes=1))
    long = service.create_access_token({"sub": "a"}, timedelta(hours=2))
    exp_short = jwt.decode(short, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])["exp"]
    exp_long = jwt.decode(long, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])["exp"]
    assert exp_long > exp_short
