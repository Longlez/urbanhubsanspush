"""
Unit tests for the validator module.
"""

import pytest
from datetime import datetime
from src.validator import LogValidator, ConfigValidator


class TestLogValidator:
    """Test cases for LogValidator class."""

    def test_validate_valid_log(self):
        """Test validation of a valid log entry."""
        valid_log = {
            "timestamp": "2024-04-26T10:30:00",
            "level": "INFO",
            "message": "Application started successfully",
            "source": "main.py"
        }
        is_valid, error = LogValidator.validate_log(valid_log)
        assert is_valid is True
        assert error is None

    def test_validate_missing_required_field(self):
        """Test validation fails when required field is missing."""
        invalid_log = {
            "timestamp": "2024-04-26T10:30:00",
            "level": "INFO",
            "message": "Application started"
        }
        is_valid, error = LogValidator.validate_log(invalid_log)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_timestamp_format(self):
        """Test validation fails with invalid timestamp format."""
        invalid_log = {
            "timestamp": "2024/04/26 10:30:00",
            "level": "INFO",
            "message": "Test message",
            "source": "test.py"
        }
        is_valid, error = LogValidator.validate_log(invalid_log)
        assert is_valid is False
        assert "Invalid timestamp format" in error

    def test_validate_invalid_log_level(self):
        """Test validation fails with invalid log level."""
        invalid_log = {
            "timestamp": "2024-04-26T10:30:00",
            "level": "INVALID",
            "message": "Test message",
            "source": "test.py"
        }
        is_valid, error = LogValidator.validate_log(invalid_log)
        assert is_valid is False
        assert "Invalid log level" in error

    def test_validate_empty_message(self):
        """Test validation fails with empty message."""
        invalid_log = {
            "timestamp": "2024-04-26T10:30:00",
            "level": "INFO",
            "message": "",
            "source": "test.py"
        }
        is_valid, error = LogValidator.validate_log(invalid_log)
        assert is_valid is False
        assert "Message must be a non-empty string" in error

    def test_validate_empty_source(self):
        """Test validation fails with empty source."""
        invalid_log = {
            "timestamp": "2024-04-26T10:30:00",
            "level": "INFO",
            "message": "Test message",
            "source": ""
        }
        is_valid, error = LogValidator.validate_log(invalid_log)
        assert is_valid is False
        assert "Source must be a non-empty string" in error

    def test_validate_all_log_levels(self):
        """Test validation with all valid log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            log = {
                "timestamp": "2024-04-26T10:30:00",
                "level": level,
                "message": f"Test {level}",
                "source": "test.py"
            }
            is_valid, error = LogValidator.validate_log(log)
            assert is_valid is True, f"Level {level} should be valid"

    def test_validate_log_batch_all_valid(self):
        """Test batch validation with all valid logs."""
        logs = [
            {
                "timestamp": "2024-04-26T10:30:00",
                "level": "INFO",
                "message": "Log 1",
                "source": "test.py"
            },
            {
                "timestamp": "2024-04-26T10:31:00",
                "level": "ERROR",
                "message": "Log 2",
                "source": "test.py"
            }
        ]
        all_valid, errors = LogValidator.validate_log_batch(logs)
        assert all_valid is True
        assert errors == []

    def test_validate_log_batch_with_errors(self):
        """Test batch validation with some invalid logs."""
        logs = [
            {
                "timestamp": "2024-04-26T10:30:00",
                "level": "INFO",
                "message": "Valid log",
                "source": "test.py"
            },
            {
                "timestamp": "invalid",
                "level": "INFO",
                "message": "Invalid log",
                "source": "test.py"
            }
        ]
        all_valid, errors = LogValidator.validate_log_batch(logs)
        assert all_valid is False
        assert len(errors) == 1
        assert errors[0]["index"] == 1


class TestConfigValidator:
    """Test cases for ConfigValidator class."""

    def test_validate_valid_rabbitmq_config(self):
        """Test validation of valid RabbitMQ configuration."""
        config = {
            "host": "localhost",
            "port": 5672,
            "username": "guest",
            "password": "guest",
            "queue": "logs"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_rabbitmq_config_key(self):
        """Test validation fails when RabbitMQ config key is missing."""
        config = {
            "host": "localhost",
            "port": 5672,
            "username": "guest",
            "password": "guest"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Missing required configuration key" in error

    def test_validate_invalid_rabbitmq_port(self):
        """Test validation fails with invalid port."""
        config = {
            "host": "localhost",
            "port": 99999,
            "username": "guest",
            "password": "guest",
            "queue": "logs"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Port must be" in error

    def test_validate_empty_rabbitmq_host(self):
        """Test validation fails with empty host."""
        config = {
            "host": "",
            "port": 5672,
            "username": "guest",
            "password": "guest",
            "queue": "logs"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Host must be" in error

    def test_validate_valid_database_config(self):
        """Test validation of valid database configuration."""
        config = {
            "url": "sqlite:///./test.db",
            "echo": False
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_database_config_key(self):
        """Test validation fails when database config key is missing."""
        config = {
            "url": "sqlite:///./test.db"
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is False
        assert "Missing required configuration key" in error

    def test_validate_invalid_database_url(self):
        """Test validation fails with invalid database URL."""
        config = {
            "url": "",
            "echo": False
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is False
        assert "Database URL must be" in error

    def test_validate_invalid_database_echo_type(self):
        """Test validation fails with invalid echo type."""
        config = {
            "url": "sqlite:///./test.db",
            "echo": "yes"
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is False
        assert "Echo setting must be a boolean" in error
