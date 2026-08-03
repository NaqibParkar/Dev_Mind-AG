def test_register_and_login(client):
    registration = client.post(
        "/auth/register",
        json={
            "email": "developer@example.com",
            "password": "correct-horse-battery-staple",
            "full_name": "Developer",
        },
    )

    assert registration.status_code == 200
    assert registration.json()["access_token"] != "mock_token_registered"

    login = client.post(
        "/auth/login",
        json={
            "email": "developer@example.com",
            "password": "correct-horse-battery-staple",
        },
    )

    assert login.status_code == 200
    assert login.json()["access_token"] != "mock_token_login"


def test_registration_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "developer@example.com", "password": "short"},
    )

    assert response.status_code == 422

