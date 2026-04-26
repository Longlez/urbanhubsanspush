"""
Validator module for ms-alerte-usager.

This module provides validation utilities for alert data and system configuration.
"""

from typing import Any, Dict, Optional
from datetime import datetime


class AlertValidator:
    """Validates alert entries according to defined rules."""

    REQUIRED_FIELDS = ["user_id", "alert_type", "message", "timestamp", "severity"]
    VALID_ALERT_TYPES = ["SECURITY", "SYSTEM", "USER", "MAINTENANCE"]
    VALID_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    @classmethod
    def validate_alert(cls, alert_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate an alert entry.

        Args:
            alert_data: Dictionary containing alert entry data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in alert_data:
                return False, f"Missing required field: {field}"

        # Validate user_id
        if not isinstance(alert_data.get("user_id"), (int, str)) or not alert_data["user_id"]:
            return False, "user_id must be a non-empty integer or string"

        # Validate alert_type
        if alert_data["alert_type"] not in cls.VALID_ALERT_TYPES:
            return False, f"Invalid alert_type: {alert_data['alert_type']}. Must be one of {cls.VALID_ALERT_TYPES}"

        # Validate severity
        if alert_data["severity"] not in cls.VALID_SEVERITIES:
            return False, f"Invalid severity: {alert_data['severity']}. Must be one of {cls.VALID_SEVERITIES}"

        # Validate timestamp format
        try:
            datetime.fromisoformat(alert_data["timestamp"])
        except (ValueError, TypeError):
            return False, "Invalid timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Validate message is not empty
        if not alert_data.get("message") or not isinstance(alert_data["message"], str):
            return False, "Message must be a non-empty string"

        return True, None

    @classmethod
    def validate_alert_batch(cls, alerts: list) -> tuple[bool, list]:
        """
        Validate a batch of alert entries.

        Args:
            alerts: List of alert entry dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, alert in enumerate(alerts):
            is_valid, error_msg = cls.validate_alert(alert)
            if not is_valid:
                errors.append({"index": idx, "error": error_msg})

        return len(errors) == 0, errors


class NotificationValidator:
    """Validates notification configurations."""

    REQUIRED_FIELDS = ["email_enabled", "sms_enabled", "webhook_url"]

    @classmethod
    def validate_notification_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate notification configuration.

        Args:
            config: Dictionary containing notification configuration

        Returns:
            Tuple of (is_valid, error_message)
        """
        for field in cls.REQUIRED_FIELDS:
            if field not in config:
                return False, f"Missing required field: {field}"

        # Validate boolean fields
        for field in ["email_enabled", "sms_enabled"]:
            if not isinstance(config.get(field), bool):
                return False, f"{field} must be a boolean value"

        # Validate webhook_url if provided
        webhook_url = config.get("webhook_url")
        if webhook_url and not isinstance(webhook_url, str):
            return False, "webhook_url must be a string"

        return True, None


class DatabaseValidator:
    """Validates database configurations."""

    @classmethod
    def validate_postgres_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate PostgreSQL configuration.

        Args:
            config: Dictionary containing PostgreSQL configuration

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ["host", "port", "database", "username", "password"]

        for key in required_keys:
            if key not in config:
                return False, f"Missing required configuration key: {key}"

        if not isinstance(config.get("port"), int) or not (0 < config["port"] < 65536):
            return False, "Port must be an integer between 1 and 65535"

        if not config.get("host"):
            return False, "Host must be a non-empty string"

        if not config.get("database"):
            return False, "Database name must be a non-empty string"

        return True, None
