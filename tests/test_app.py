import string
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient

from flask_app import app as app_module

SYMBOLS = "!@#$%^&*()_+"


@pytest.fixture
def client() -> FlaskClient:
    return app_module.app.test_client()


def _limits_text() -> str:
    return f"от {app_module.MIN_LENGTH} до {app_module.MAX_LENGTH}"


class TestGenerateEndpoint:
    def test_length_below_min_returns_400(self, client: FlaskClient) -> None:
        length = app_module.MIN_LENGTH - 1
        response = client.get(f"/generate?length={length}")
        assert response.status_code == 400
        assert _limits_text() in response.get_data(as_text=True)

    def test_length_above_max_returns_400(self, client: FlaskClient) -> None:
        length = app_module.MAX_LENGTH + 1
        response = client.get(f"/generate?length={length}")
        assert response.status_code == 400
        assert _limits_text() in response.get_data(as_text=True)

    def test_non_numeric_length_returns_400(self, client: FlaskClient) -> None:
        response = client.get("/generate?length=abc")
        assert response.status_code == 400
        assert _limits_text() in response.get_data(as_text=True)

    def test_min_length_is_accepted(self, client: FlaskClient) -> None:
        response = client.get(f"/generate?length={app_module.MIN_LENGTH}")
        assert response.status_code == 200

    def test_max_length_is_accepted(self, client: FlaskClient) -> None:
        response = client.get(f"/generate?length={app_module.MAX_LENGTH}")
        assert response.status_code == 200

    def test_internal_error_returns_500_without_details(
        self, client: FlaskClient
    ) -> None:
        with patch(
            "flask_app.app.generate_password",
            side_effect=RuntimeError("секрет-деталь"),
        ):
            response = client.get("/generate?length=12")
        assert response.status_code == 500
        assert "секрет-деталь" not in response.get_data(as_text=True)

    def test_regenerate_link_keeps_all_params(self, client: FlaskClient) -> None:
        html = client.get(
            "/generate?length=12&use_upper=on&use_digits=on&use_symbols=on"
        ).get_data(as_text=True)
        expected = 'href="/generate?length=12&amp;use_upper=on&amp;use_digits=on'
        assert expected in html

    def test_regenerate_link_does_not_add_unchecked_params(
        self, client: FlaskClient
    ) -> None:
        html = client.get("/generate?length=8").get_data(as_text=True)
        assert 'href="/generate?length=8"' in html


class TestGeneratePassword:
    def test_contains_every_requested_type(self) -> None:
        length = 4
        for _ in range(300):
            password = app_module.generate_password(length, True, True, True)
            assert len(password) == length
            assert any(c in string.ascii_lowercase for c in password)
            assert any(c in string.ascii_uppercase for c in password)
            assert any(c in string.digits for c in password)
            assert any(c in SYMBOLS for c in password)

    def test_only_lowercase_when_all_flags_off(self) -> None:
        password = app_module.generate_password(12, False, False, False)
        assert all(c in string.ascii_lowercase for c in password)

    def test_length_is_exact(self) -> None:
        assert len(app_module.generate_password(12, True, True, True)) == 12

    def test_length_less_than_required_types_raises(self) -> None:
        with pytest.raises(ValueError):
            app_module.generate_password(2, True, True, True)


class TestHome:
    def test_form_has_length_limits(self, client: FlaskClient) -> None:
        html = client.get("/").get_data(as_text=True)
        assert f'min="{app_module.MIN_LENGTH}"' in html
        assert f'max="{app_module.MAX_LENGTH}"' in html
