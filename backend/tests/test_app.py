from pathlib import Path

from disc_golf_tracker.config import Settings
from disc_golf_tracker.main import create_app
from fastapi.testclient import TestClient


def settings(tmp_path: Path) -> Settings:
    return Settings(
        environment="test",
        secret_key="test-secret-key-with-at-least-32-characters",
        bootstrap_token="one-time-bootstrap-token",
        data_dir=tmp_path,
        static_dir=tmp_path / "static",
        access_token_minutes=60,
        trusted_hosts=("testserver",),
    )


def test_health_checks(tmp_path: Path) -> None:
    with TestClient(create_app(settings(tmp_path))) as client:
        assert client.get("/api/health/live").json() == {"status": "ok"}
        assert client.get("/api/health/ready").json() == {"status": "ready"}


def test_bootstrap_is_one_time_and_login_works(tmp_path: Path) -> None:
    with TestClient(create_app(settings(tmp_path))) as client:
        assert client.get("/api/auth/bootstrap-status").json() == {"bootstrap_required": True}
        response = client.post(
            "/api/auth/bootstrap",
            headers={"X-Bootstrap-Token": "one-time-bootstrap-token"},
            json={
                "username": "owner",
                "display_name": "Course Owner",
                "password": "correct horse battery staple",
            },
        )
        assert response.status_code == 201
        token = response.json()["access_token"]
        assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json() == {
            "id": client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json()[
                "id"
            ],
            "username": "owner",
            "display_name": "Course Owner",
            "is_admin": True,
        }
        assert (
            client.post(
                "/api/auth/bootstrap",
                headers={"X-Bootstrap-Token": "one-time-bootstrap-token"},
                json={
                    "username": "second",
                    "display_name": "Second",
                    "password": "another long secure password",
                },
            ).status_code
            == 409
        )
        assert (
            client.post(
                "/api/auth/login",
                json={"username": "owner", "password": "correct horse battery staple"},
            ).status_code
            == 200
        )


def test_bootstrap_rejects_wrong_token(tmp_path: Path) -> None:
    with TestClient(create_app(settings(tmp_path))) as client:
        response = client.post(
            "/api/auth/bootstrap",
            headers={"X-Bootstrap-Token": "wrong"},
            json={
                "username": "owner",
                "display_name": "Owner",
                "password": "correct horse battery staple",
            },
        )
        assert response.status_code == 403
