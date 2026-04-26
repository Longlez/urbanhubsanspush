"""
Unit tests for the validator module.
"""

import pytest
from datetime import datetime
from src.validator import AlertValidator, NotificationValidator, DatabaseValidator


class TestAlertValidator:
    """Test cases for AlertValidator class."""

    def test_validate_valid_alert(self):
        """Test validation of a valid alert entry."""
        valid_alert = {
            "user_id": 123,
            "alert_type": "SECURITY",
            "message": "Unauthorized access detected",
            "timestamp": "2024-04-26T10:30:00",
            "severity": "HIGH"
        }
        is_valid, error = AlertValidator.validate_alert(valid_alert)
        assert is_valid is True
        assert error is None

    def test_validate_missing_required_field(self):
        """Test validation fails when required field is missing."""
        invalid_alert = {
            "user_id": 123,
            "alert_type": "SECURITY",
            "message": "Unauthorized access detected",
            "timestamp": "2024-04-26T10:30:00"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_alert_type(self):
        """Test validation fails with invalid alert type."""
        invalid_alert = {
            "user_id": 123,
            "alert_type": "INVALID",
            "message": "Test alert",
            "timestamp": "2024-04-26T10:30:00",
            "severity": "HIGH"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "Invalid alert_type" in error

    def test_validate_invalid_severity(self):
        """Test validation fails with invalid severity."""
        invalid_alert = {
            "user_id": 123,
            "alert_type": "SECURITY",
            "message": "Test alert",
            "timestamp": "2024-04-26T10:30:00",
            "severity": "INVALID"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "Invalid severity" in error

    def test_validate_invalid_timestamp_format(self):
        """Test validation fails with invalid timestamp format."""
        invalid_alert = {
            "user_id": 123,
            "alert_type": "SECURITY",
            "message": "Test alert",
            "timestamp": "2024/04/26 10:30:00",
            "severity": "HIGH"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "Invalid timestamp format" in error

    def test_validate_empty_message(self):
        """Test validation fails with empty message."""
        invalid_alert = {
            "user_id": 123,
            "alert_type": "SECURITY",
            "message": "",
            "timestamp": "2024-04-26T10:30:00",
            "severity": "HIGH"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "Message must be a non-empty string" in error

    def test_validate_invalid_user_id(self):
        """Test validation fails with invalid user_id."""
        invalid_alert = {
            "user_id": "",
            "alert_type": "SECURITY",
            "message": "Test alert",
            "timestamp": "2024-04-26T10:30:00",
            "severity": "HIGH"
        }
        is_valid, error = AlertValidator.validate_alert(invalid_alert)
        assert is_valid is False
        assert "user_id must be a non-empty" in error

    def test_validate_all_alert_types_and_severities(self):
        """Test validation with all valid alert types and severities."""
        for alert_type in ["SECURITY", "SYSTEM", "USER", "MAINTENANCE"]:
            for severity in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
                alert = {
                    "user_id": 123,
                    "alert_type": alert_type,
                    "message": f"Test {alert_type} {severity}",
                    "timestamp": "2024-04-26T10:30:00",
                    "severity": severity
                }
                is_valid, error = AlertValidator.validate_alert(alert)
                assert is_valid is True, f"Alert type {alert_type} with severity {severity} should be valid"

    def test_validate_alert_batch_all_valid(self):
        """Test batch validation with all valid alerts."""
        alerts = [
            {
                "user_id": 123,
                "alert_type": "SECURITY",
                "message": "Alert 1",
                "timestamp": "2024-04-26T10:30:00",
                "severity": "HIGH"
            },
            {
                "user_id": 456,
                "alert_type": "SYSTEM",
                "message": "Alert 2",
                "timestamp": "2024-04-26T10:31:00",
                "severity": "MEDIUM"
            }
        ]
        all_valid, errors = AlertValidator.validate_alert_batch(alerts)
        assert all_valid is True
        assert errors == []

    def test_validate_alert_batch_with_errors(self):
        """Test batch validation with some invalid alerts."""
        alerts = [
            {
                "user_id": 123,
                "alert_type": "SECURITY",
                "message": "Valid alert",
                "timestamp": "2024-04-26T10:30:00",
                "severity": "HIGH"
            },
            {
                "user_id": "",
                "alert_type": "INVALID",
                "message": "Invalid alert",
                "timestamp": "invalid",
                "severity": "INVALID"
            }
        ]
        all_valid, errors = AlertValidator.validate_alert_batch(alerts)
        assert all_valid is False
        assert len(errors) == 1
        assert errors[0]["index"] == 1


class TestNotificationValidator:
    """Test cases for NotificationValidator class."""

    def test_validate_valid_notification_config(self):
        """Test validation of valid notification configuration."""
        config = {
            "email_enabled": True,
            "sms_enabled": False,
            "webhook_url": "https://example.com/webhook"
        }
        is_valid, error = NotificationValidator.validate_notification_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_notification_config_key(self):
        """Test validation fails when notification config key is missing."""
        config = {
            "email_enabled": True,
            "sms_enabled": False
        }
        is_valid, error = NotificationValidator.validate_notification_config(config)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_boolean_field(self):
        """Test validation fails with invalid boolean field."""
        config = {
            "email_enabled": "yes",
            "sms_enabled": False,
            "webhook_url": "https://example.com/webhook"
        }
        is_valid, error = NotificationValidator.validate_notification_config(config)
        assert is_valid is False
        assert "email_enabled must be a boolean" in error

    def test_validate_invalid_webhook_url_type(self):
        """Test validation fails with invalid webhook_url type."""
        config = {
            "email_enabled": True,
            "sms_enabled": False,
            "webhook_url": 12345
        }
        is_valid, error = NotificationValidator.validate_notification_config(config)
        assert is_valid is False
        assert "webhook_url must be a string" in error


class TestDatabaseValidator:
    """Test cases for DatabaseValidator class."""

    def test_validate_valid_postgres_config(self):
        """Test validation of valid PostgreSQL configuration."""
        config = {
            "host": "localhost",
            "port": 5432,
            "database": "alerts",
            "username": "user",
            "password": "password"
        }
        is_valid, error = DatabaseValidator.validate_postgres_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_postgres_config_key(self):
        """Test validation fails when PostgreSQL config key is missing."""
        config = {
            "host": "localhost",
            "port": 5432,
            "database": "alerts",
            "username": "user"
        }
        is_valid, error = DatabaseValidator.validate_postgres_config(config)
        assert is_valid is False
        assert "Missing required configuration key" in error

    def test_validate_invalid_postgres_port(self):
        """Test validation fails with invalid port."""
        config = {
            "host": "localhost",
            "port": 99999,
            "database": "alerts",
            "username": "user",
            "password": "password"
        }
        is_valid, error = DatabaseValidator.validate_postgres_config(config)
        assert is_valid is False
        assert "Port must be" in error

    def test_validate_empty_postgres_host(self):
        """Test validation fails with empty host."""
        config = {
            "host": "",
            "port": 5432,
            "database": "alerts",
            "username": "user",
            "password": "password"
        }
        is_valid, error = DatabaseValidator.validate_postgres_config(config)
        assert is_valid is False
        assert "Host must be" in error

    def test_validate_empty_postgres_database(self):
        """Test validation fails with empty database name."""
        config = {
            "host": "localhost",
            "port": 5432,
            "database": "",
            "username": "user",
            "password": "password"
        }
        is_valid, error = DatabaseValidator.validate_postgres_config(config)
        assert is_valid is False
        assert "Database name must be" in error
