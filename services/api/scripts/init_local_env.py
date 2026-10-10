"""Create local-only credentials once; never overwrite an existing environment."""

import secrets
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    password = secrets.token_urlsafe(32)
    user, database = "citysense", "citysense"
    base = f"postgresql://{user}:{password}@127.0.0.1:55432/"
    contents = "\n".join(
        [
            "# Generated local development settings. Excluded from version control.",
            f"POSTGRES_USER={user}",
            f"POSTGRES_DB={database}",
            f"POSTGRES_PASSWORD={password}",
            f"CITYSENSE_DATABASE_URL={base}{database}",
            f"CITYSENSE_TEST_DATABASE_URL={base}{database}_test",
            "CITYSENSE_MODE=development",
            "CITYSENSE_API_KEY=",
            "CITYSENSE_RATE_LIMIT=60",
            "CITYSENSE_BODY_LIMIT=262144",
            "",
        ]
    )
    with (root / ".env").open("x", encoding="utf-8") as environment:
        environment.write(contents)
    print("Created .env with local credentials. Existing files are never overwritten.")


if __name__ == "__main__":
    main()
