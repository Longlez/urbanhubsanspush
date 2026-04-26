"""
Validator module for ms-journalisation.

This module provides validation utilities for log data and system configuration.
"""

from typing import Any, Dict, Optional
from datetime import datetime


class LogValidator:
    """Validates log entries according to defined rules."""

    REQUIRED_FIELDS = ["timestamp", "level", "message", "source"]
    VALID_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def validate_log(cls, log_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate a log entry.

        Args:
            log_data: Dictionary containing log entry data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in log_data:
                return False, f"Missing required field: {field}"

        # Validate timestamp format
        try:
            datetime.fromisoformat(log_data["timestamp"])
        except (ValueError, TypeError):
            return False, "Invalid timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Validate log level
        if log_data["level"] not in cls.VALID_LEVELS:
            return False, f"Invalid log level: {log_data['level']}. Must be one of {cls.VALID_LEVELS}"

        # Validate message is not empty
        if not log_data.get("message") or not isinstance(log_data["message"], str):
            return False, "Message must be a non-empty string"

        # Validate source is not empty
        if not log_data.get("source") or not isinstance(log_data["source"], str):
            return False, "Source must be a non-empty string"

        return True, None

    @classmethod
    def validate_log_batch(cls, logs: list) -> tuple[bool, list]:
        """
        Validate a batch of log entries.

        Args:
            logs: List of log entry dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, log in enumerate(logs):
            is_valid, error_msg = cls.validate_log(log)
            if not is_valid:
                errors.append({"index": idx, "error": error_msg})

        return len(errors) == 0, errors


class ConfigValidator:
    """Validates system configuration."""

    @classmethod
    def validate_rabbitmq_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate RabbitMQ configuration.

        Args:
            config: Dictionary containing RabbitMQ configuration

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ["host", "port", "username", "password", "queue"]

        for key in required_keys:
            if key not in config:
                return False, f"Missing required configuration key: {key}"

        if not isinstance(config.get("port"), int) or not (0 < config["port"] < 65536):
            return False, "Port must be an integer between 1 and 65535"

        if not config.get("host"):
            return False, "Host must be a non-empty string"

        return True, None

    @classmethod
    def validate_database_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate database configuration.

        Args:
            config: Dictionary containing database configuration

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ["url", "echo"]

        for key in required_keys:
            if key not in config:
                return False, f"Missing required configuration key: {key}"

        if not isinstance(config.get("url"), str) or not config["url"]:
            return False, "Database URL must be a non-empty string"

        if not isinstance(config.get("echo"), bool):
            return False, "Echo setting must be a boolean value"

        return True, None
