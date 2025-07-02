"""
Direct Oracle connection test without SQLAlchemy.
"""

import os

import oracledb
from dotenv import load_dotenv

# Load environment
load_dotenv()


def test_direct_connection():
    """Test direct oracledb connection."""

    # Get connection parameters
    host = os.getenv("DATABASE__HOST")
    port = int(os.getenv("DATABASE__PORT", "1521"))
    service_name = os.getenv("DATABASE__SERVICE_NAME")
    username = os.getenv("DATABASE__USERNAME")
    password = os.getenv("DATABASE__PASSWORD")
    protocol = os.getenv("DATABASE__PROTOCOL", "tcp")

    print(f"Connecting to {protocol}://{host}:{port}/{service_name}")

    # Build DSN
    if protocol == "tcps":
        # For TCPS with IP address, we need to disable SSL verification
        dsn = f"""(DESCRIPTION=
            (ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))
            (CONNECT_DATA=(SERVICE_NAME={service_name}))
            (SECURITY=(SSL_SERVER_DN_MATCH=NO))
        )"""
    else:
        dsn = f"{host}:{port}/{service_name}"

    print(f"DSN: {dsn}")

    try:
        # Connect with ssl_server_dn_match=False for IP connections
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn,
            ssl_server_dn_match=False,  # Important for IP-based connections
        )

        print("Connection successful!")

        # Test query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            print(f"Query result: {result}")

            # Check version
            cursor.execute("SELECT BANNER FROM v$version WHERE ROWNUM = 1")
            version = cursor.fetchone()
            print(f"Oracle version: {version}")

        connection.close()

    except Exception as e:
        print(f"Connection failed: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    test_direct_connection()
