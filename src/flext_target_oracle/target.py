"""Oracle Target - Main Singer Target Implementation.

Clean implementation using flext-core and flext-infrastructure.databases.flext-db-oracle foundations.
Zero duplication, enterprise-grade performance.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from flext_core import ServiceResult
from flext_observability.logging import get_logger

from flext_target_oracle.application.services import SingerTargetService
from flext_target_oracle.domain.models import LoadStatistics, TargetConfig

logger = get_logger(__name__)


class OracleTarget:
    """Main Oracle Singer Target implementation."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize Oracle target with configuration."""
        self.config = TargetConfig(**(config or {}))
        self.target_service = SingerTargetService(self.config)
        self._running = False

    async def run_async(self) -> ServiceResult[None]:
        """Run target in async mode (preferred)."""
        try:
            self._running = True
            logger.info("Oracle target started (async mode)")

            # Process all stdin messages
            result = await self._process_stdin_messages()
            if not result.is_success:
                return result

            # Finalize streams
            return await self._finalize_streams()

        except Exception as e:
            logger.exception("Target execution failed")
            return ServiceResult.fail(f"Target execution failed: {e}")
        finally:
            self._running = False

    async def _process_stdin_messages(self) -> ServiceResult[None]:
        """Process Singer messages from stdin."""
        line_count = 0
        error_count = 0
        progress_interval = 10

        for line in sys.stdin:
            if not self._running:
                break

            stripped_line = line.strip()
            if not stripped_line:
                continue

            # Skip non-JSON lines (log messages, etc.)
            if not stripped_line.startswith("{"):
                continue

            try:
                # Parse and process message
                message = json.loads(stripped_line)
                process_result = await self._process_single_message(
                    message,
                    line_count + 1,
                )

                if not process_result.is_success:
                    error_count += 1

                line_count += 1

                # Log progress periodically
                if line_count % progress_interval == 0:
                    logger.info(
                        "Processed %d messages (%d errors)",
                        line_count,
                        error_count,
                    )

            except json.JSONDecodeError:
                logger.debug("Skipped invalid JSON line: %s", stripped_line[:100])
                # Don't count as error since it might be a log message
                continue
            except Exception:
                logger.exception("Unexpected error processing message")
                error_count += 1

        return ServiceResult.ok(None)

    async def _process_single_message(
        self,
        message: dict[str, Any],
        message_number: int,
    ) -> ServiceResult[None]:
        """Process a single Singer message."""
        msg_type = message.get("type", "UNKNOWN")
        logger.debug("Processing message %d: type=%s", message_number, msg_type)

        # Log message-specific details
        self._log_message_details(message, msg_type)

        # Process message
        result = await self.target_service.process_singer_message(message)

        if not result.is_success:
            logger.error("Failed to process message: %s", result.error)
        else:
            logger.debug("Successfully processed %s message", msg_type)

        return result

    def _log_message_details(self, message: dict[str, Any], msg_type: str) -> None:
        """Log message-specific details for debugging."""
        if msg_type == "SCHEMA":
            logger.info("SCHEMA message for stream: %s", message.get("stream"))
            schema_props = message.get("schema", {}).get("properties", {})
            logger.debug("Schema properties: %s", list(schema_props.keys()))
        elif msg_type == "RECORD":
            stream = message.get("stream")
            record_id = message.get("record", {}).get("id")
            logger.debug("RECORD for stream: %s, id=%s", stream, record_id)

    async def _finalize_streams(self) -> ServiceResult[None]:
        """Finalize all streams and log statistics."""
        logger.info("Finalizing streams...")
        finalize_result = await self.target_service.finalize_all_streams()

        if finalize_result.is_success:
            stats = finalize_result.value
            if stats is not None:
                self._log_completion_stats(stats)
            return ServiceResult.ok(None)
        error_msg = f"Finalization failed: {finalize_result.error}"
        logger.error("Finalization failed: %s", finalize_result.error)
        return ServiceResult.fail(error_msg)

    def _log_completion_stats(self, stats: LoadStatistics) -> None:
        """Log completion statistics."""
        logger.info("Target completed successfully:")
        logger.info("  Total records: %d", stats.total_records)
        logger.info("  Successful: %d", stats.successful_records)
        logger.info("  Failed: %d", stats.failed_records)
        logger.info("  Success rate: %.2f%%", stats.success_rate)

    def run(self) -> int:
        """Run target in sync mode (Singer standard)."""
        try:
            # Run async method in event loop
            result = asyncio.run(self.run_async())

            if result.is_success:
                logger.info("Oracle target completed successfully")
                return 0
            logger.error("Oracle target failed: %s", result.error)
            return 1

        except KeyboardInterrupt:
            logger.info("Target interrupted by user")
            self._running = False
            return 130
        except Exception:
            logger.exception("Unexpected error")
            return 1

    def stop(self) -> None:
        """Stop the target gracefully."""
        logger.info("Stopping Oracle target...")
        self._running = False


def main() -> int:
    """Run Singer target with CLI arguments."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Oracle Singer Target")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--state", type=str, help="Path to state file")
    args = parser.parse_args()

    # Load configuration
    config = {}

    # First, check if config file is provided
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            with config_path.open(encoding="utf-8") as f:
                config = json.load(f)
            logger.info("Loaded config from file: %s", args.config)

    # Then, override with environment variables if present
    env_config: dict[str, str | int | None] = {
        "host": os.getenv("FLEXT_TARGET_ORACLE_HOST"),
        "port": os.getenv("FLEXT_TARGET_ORACLE_PORT"),
        "service_name": os.getenv("FLEXT_TARGET_ORACLE_SERVICE_NAME"),
        "sid": os.getenv("FLEXT_TARGET_ORACLE_SID"),
        "username": os.getenv("FLEXT_TARGET_ORACLE_USERNAME"),
        "password": os.getenv("FLEXT_TARGET_ORACLE_PASSWORD"),
        "protocol": os.getenv("FLEXT_TARGET_ORACLE_PROTOCOL"),
        "default_target_schema": os.getenv("FLEXT_TARGET_ORACLE_SCHEMA"),
        "table_prefix": os.getenv("FLEXT_TARGET_ORACLE_TABLE_PREFIX"),
        "batch_size": os.getenv("FLEXT_TARGET_ORACLE_BATCH_SIZE"),
        "max_parallelism": os.getenv("FLEXT_TARGET_ORACLE_MAX_PARALLELISM"),
    }

    # Convert port, batch_size, and max_parallelism to int if present
    for key in ["port", "batch_size", "max_parallelism"]:
        value = env_config.get(key)
        if value:
            try:
                env_config[key] = int(value)
            except ValueError:
                logger.warning("Invalid %s value in environment: %s", key, value)
                env_config[key] = None

    # Merge environment config over file config
    for k, v in env_config.items():
        if v is not None:
            config[k] = v

    # Apply defaults if not set
    config.setdefault("host", "localhost")
    config.setdefault("port", 1521)
    config.setdefault("protocol", "tcp")
    config.setdefault("default_target_schema", "SINGER_DATA")
    config.setdefault("table_prefix", "")
    config.setdefault("batch_size", 10000)
    config.setdefault("max_parallelism", 4)

    # Debug print
    try:
        target = OracleTarget(config)
        return target.run()
    except Exception:
        logger.exception("Failed to start Oracle target")
        return 1


if __name__ == "__main__":
    sys.exit(main())
