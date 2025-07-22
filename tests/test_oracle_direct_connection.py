# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Direct Oracle connection test without SQLAlchemy."""

import os

import oracledb
from dotenv import load_dotenv

# Load environment
load_dotenv()


def test_direct_connection() -> None:
    """Test direct Oracle database connection with environment configuration."""
    host = os.getenv("DATABASE__HOST")
    port = int(os.getenv("DATABASE__PORT", "1521"))
    service_name = os.getenv("DATABASE__SERVICE_NAME")
    username = os.getenv("DATABASE__USERNAME")
    password = os.getenv("DATABASE__PASSWORD")
    protocol = os.getenv("DATABASE__PROTOCOL", "tcp")

    # Build DSN
    if (
        protocol == "tcps"
    ):  # For TCPS with IP address, we need to disable SSL verification
        dsn = f"""(DESCRIPTION=
            (ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))
            (CONNECT_DATA=(SERVICE_NAME={service_name}))
            (SECURITY=(SSL_SERVER_DN_MATCH=NO))
        )"""
    else:
        dsn = f"{host}:{port}/{service_name}"

    try:  # Connect with ssl_server_dn_match=False for IP connections
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn,
            ssl_server_dn_match=False,  # Important for IP-based connections
        )

        # Test query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            cursor.fetchone()

            # Check version
            cursor.execute("SELECT BANNER FROM v$version WHERE ROWNUM = 1")
            cursor.fetchone()

        connection.close()

    except Exception as e:
        msg = f"Connection failed: {e}"
        raise AssertionError(msg) from e


if __name__ == "__main__":
    test_direct_connection()
