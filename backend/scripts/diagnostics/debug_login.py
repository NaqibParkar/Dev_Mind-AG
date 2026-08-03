import argparse
from getpass import getpass

import requests


def check_login(base_url: str, email: str, password: str) -> None:
    response = requests.post(
        f"{base_url.rstrip('/')}/auth/login",
        json={"email": email, "password": password},
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    print(f"Status code: {response.status_code}")
    if response.ok:
        print("Login succeeded.")
    else:
        print("Login failed. Response body is intentionally not printed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()
    check_login(args.base_url, args.email, getpass("Password: "))
