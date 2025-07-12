# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test SQLAlchemy connection to Oracle Autonomous Database."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment
load_dotenv()


def test_sqlalchemy_connection() -> None: # Get connection parameters
    host = os.getenv("DATABASE__HOST")
    port = int(os.getenv("DATABASE__PORT", "1521"))
    service_name = os.getenv("DATABASE__SERVICE_NAME")
    username = os.getenv("DATABASE__USERNAME")
    password = os.getenv("DATABASE__PASSWORD")
    os.getenv("DATABASE__PROTOCOL", "tcp")

    # Build DSN for TCPS
    dsn = f"""(DESCRIPTION=
        (ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))
        (CONNECT_DATA=(SERVICE_NAME={service_name}))
    )"""

    # Remove quotes from password if present: if password.startswith('"') and password.endswith('"'): password = password[1:-1]

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
    with engine.connect() as conn: conn.execute(text("SELECT 1 FROM DUAL")).scalar()

        conn.execute(
            text("SELECT BANNER FROM v$version WHERE ROWNUM = 1"),
        ).scalar()

        # Check user and schema
        conn.execute(text("SELECT USER FROM DUAL")).scalar()

        # Check if we're on Enterprise Edition: conn.execute(
            text(
                """
            SELECT COUNT(*) FROM v$version
            WHERE BANNER LIKE '%Enterprise Edition%'
        """
            ),
        ).scalar()
        # Note: enterprise_count > 0 indicates Enterprise Edition


if __name__ == "__main__":
                test_sqlalchemy_connection()
