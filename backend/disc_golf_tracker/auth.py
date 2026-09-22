from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pwdlib import PasswordHash
from pydantic import BaseModel, Field

from .config import Settings
from .database import Database

router = APIRouter(prefix="/api/auth", tags=["authentication"])
password_hash = PasswordHash.recommended()


class BootstrapRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_.-]+$")
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=12, max_length=256)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: str
    username: str
    display_name: str
    is_admin: bool


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def _database(request: Request) -> Database:
    return request.app.state.database


def _token(user_id: str, settings: Settings) -> TokenResponse:
    now = datetime.now(UTC)
    expires = now + timedelta(minutes=settings.access_token_minutes)
    encoded = jwt.encode(
        {"sub": user_id, "iat": now, "exp": expires, "jti": str(uuid4())},
        settings.secret_key,
        algorithm="HS256",
    )
    return TokenResponse(access_token=encoded, expires_in=settings.access_token_minutes * 60)


@router.get("/bootstrap-status")
def bootstrap_status(database: Database = Depends(_database)) -> dict[str, bool]:
    with database.session() as connection:
        has_users = connection.execute("SELECT EXISTS(SELECT 1 FROM users)").fetchone()[0]
    return {"bootstrap_required": not bool(has_users)}


@router.post("/bootstrap", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def bootstrap(
    payload: BootstrapRequest,
    x_bootstrap_token: str | None = Header(default=None),
    settings: Settings = Depends(_settings),
    database: Database = Depends(_database),
) -> TokenResponse:
    if not settings.bootstrap_token or x_bootstrap_token != settings.bootstrap_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid bootstrap token")
    with database.session() as connection:
        # Reserve the write lock before checking. Two first-run requests must never
        # both observe an empty user table and create administrators.
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute("SELECT EXISTS(SELECT 1 FROM users)").fetchone()[0]:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bootstrap is closed")
        user_id = str(uuid4())
        connection.execute(
            """INSERT INTO users
               (id, username, display_name, password_hash, is_admin, created_at)
               VALUES (?, ?, ?, ?, 1, ?)""",
            (
                user_id,
                payload.username,
                payload.display_name,
                password_hash.hash(payload.password),
                datetime.now(UTC).isoformat(),
            ),
        )
    return _token(user_id, settings)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    settings: Settings = Depends(_settings),
    database: Database = Depends(_database),
) -> TokenResponse:
    with database.session() as connection:
        user = connection.execute(
            "SELECT id, password_hash, is_active FROM users WHERE username = ?", (payload.username,)
        ).fetchone()
    if (
        not user
        or not user["is_active"]
        or not password_hash.verify(payload.password, user["password_hash"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _token(user["id"], settings)


def current_user(
    request: Request,
    authorization: str | None = Header(default=None),
) -> UserResponse:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    try:
        payload = jwt.decode(
            authorization.removeprefix("Bearer "),
            request.app.state.settings.secret_key,
            algorithms=["HS256"],
        )
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from error
    with request.app.state.database.session() as connection:
        user = connection.execute(
            "SELECT id, username, display_name, is_admin FROM users WHERE id = ? AND is_active = 1",
            (payload["sub"],),
        ).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unavailable")
    return UserResponse(
        id=user["id"],
        username=user["username"],
        display_name=user["display_name"],
        is_admin=bool(user["is_admin"]),
    )


@router.get("/me", response_model=UserResponse)
def me(user: UserResponse = Depends(current_user)) -> UserResponse:
    return user
