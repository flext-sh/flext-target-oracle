"""
Test SQLAlchemy connection to Oracle Autonomous Database.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment
load_dotenv()


def test_sqlalchemy_connection() -> None:
    """Test SQLAlchemy connection to Oracle Autonomous Database."""

    # Get connection parameters
    host = os.getenv("DATABASE__HOST")
    port = int(os.getenv("DATABASE__PORT", "1521"))
    service_name = os.getenv("DATABASE__SERVICE_NAME")
    username = os.getenv("DATABASE__USERNAME")
    password = os.getenv("DATABASE__PASSWORD")
    protocol = os.getenv("DATABASE__PROTOCOL", "tcp")

    print(f"Connecting to {protocol}://{host}:{port}/{service_name}")

    # Build DSN for TCPS
    dsn = f"""(DESCRIPTION=
        (ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))
        (CONNECT_DATA=(SERVICE_NAME={service_name}))
    )"""

    # Remove quotes from password if present
    if password.startswith('"') and password.endswith('"'):
        password = password[1:-1]

    # Create engine with connect_args
    engine = create_engine(
        "oracle+oracledb://@",
        connect_args={
            "user": username,
            "password": password,
            "dsn": dsn,
            "ssl_server_dn_match": False,
        },
    )

    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM DUAL")).scalar()
        print(f"Query result: {result}")

        version = conn.execute(
            text("SELECT BANNER FROM v$version WHERE ROWNUM = 1")
        ).scalar()
        print(f"Oracle version: {version}")

        # Check user and schema
        user = conn.execute(text("SELECT USER FROM DUAL")).scalar()
        print(f"Connected as: {user}")

        # Check if we're on Enterprise Edition
        is_ee = (
            conn.execute(
                text(
                    """
            SELECT COUNT(*) FROM v$version
            WHERE BANNER LIKE '%Enterprise Edition%'
        """
                )
            ).scalar()
            > 0
        )
        print(f"Is Enterprise Edition: {is_ee}")


if __name__ == "__main__":
    test_sqlalchemy_connection()
