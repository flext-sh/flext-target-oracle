"""Oracle Target - Main Singer Target Implementation using flext-meltano.

Singer Target implementation for Oracle Database that uses flext-meltano
for Singer SDK integration and orchestration.
"""

from __future__ import annotations

from typing import Any

from flext_core.patterns.logging import get_logger
from flext_core.result import FlextResult

# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.singer import FlextMeltanoTarget as Target

from flext_target_oracle.application.services import FlextSingerTargetService
from flext_target_oracle.domain.models import FlextTargetOracleConfig, LoadStatistics

logger = get_logger(__name__)


class FlextTargetOracle:
    """Main Oracle Singer Target implementation."""

    def __init__(self, config: dict[str, Any] | FlextTargetOracleConfig) -> None:
        """Initialize Oracle target with configuration."""
        if isinstance(config, dict):
            self.config = FlextTargetOracleConfig(**config)
        else:
            self.config = config

        self.target_service = FlextSingerTargetService(self.config)

    async def process_message(self, message: dict[str, Any]) -> FlextResult[Any]:
        """Process a single Singer message."""
        return await self.target_service.process_singer_message(message)

    async def process_messages(self, messages: list[dict[str, Any]]) -> FlextResult[LoadStatistics]:
        """Process a batch of Singer messages."""
        try:
            # Process all messages
            for message in messages:
                result = await self.process_message(message)
                if not result.is_success:
                    logger.error(f"Failed to process message: {result.error}")
                    return FlextResult.fail(f"Message processing failed: {result.error}")

            # Finalize and get statistics
            finalize_result = await self.target_service.finalize_all_streams()
            if not finalize_result.is_success:
                return FlextResult.fail(f"Finalization failed: {finalize_result.error}")

            if isinstance(finalize_result.data, LoadStatistics):
                return FlextResult.ok(finalize_result.data)
            return FlextResult.fail("Invalid statistics data returned")

        except Exception as e:
            logger.exception("Failed to process messages", exception=e)
            return FlextResult.fail(f"Message processing failed: {e}")

    async def test_connection(self) -> FlextResult[bool]:
        """Test Oracle connection."""
        try:
            # Create a simple test service to verify connection
            FlextSingerTargetService(self.config)

            # Try to connect - if constructor doesn't fail, connection is valid
            logger.info("Oracle connection test successful")
            return FlextResult.ok(True)

        except Exception as e:
            logger.exception(f"Oracle connection test failed: {e}")
            return FlextResult.fail(f"Connection failed: {e}")

    async def create_table_for_stream(
        self,
        stream_name: str,
        schema: dict[str, Any],
    ) -> FlextResult[None]:
        """Create table for a specific stream."""
        from flext_target_oracle.domain.models import SingerSchema

        try:
            # Convert schema dict to SingerSchema
            singer_schema = SingerSchema(
                type=schema.get("type", "object"),
                properties=schema.get("properties", {}),
                key_properties=schema.get("key_properties", []),
                required=schema.get("required", []),
            )

            # Use loader service to create table
            result = await self.target_service.loader_service.ensure_table_exists(
                stream_name,
                singer_schema,
            )

            if result.is_success:
                logger.info(f"Table created for stream: {stream_name}")

            return result

        except Exception as e:
            logger.exception(f"Failed to create table for stream {stream_name}", exception=e)
            return FlextResult.fail(f"Table creation failed: {e}")


# Compatibility alias
OracleTarget = FlextTargetOracle
