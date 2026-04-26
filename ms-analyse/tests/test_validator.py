"""
Unit tests for the validator module.
"""

import pytest
from datetime import datetime
from src.validator import AnalysisValidator, MetricValidator, ConfigValidator


class TestAnalysisValidator:
    """Test cases for AnalysisValidator class."""

    def test_validate_valid_analysis(self):
        """Test validation of a valid analysis entry."""
        valid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "SENSOR",
            "timestamp": "2024-04-26T10:30:00",
            "status": "COMPLETED",
            "result": {"temperature": 25.5, "humidity": 60}
        }
        is_valid, error = AnalysisValidator.validate_analysis(valid_analysis)
        assert is_valid is True
        assert error is None

    def test_validate_missing_required_field(self):
        """Test validation fails when required field is missing."""
        invalid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "SENSOR",
            "timestamp": "2024-04-26T10:30:00",
            "status": "COMPLETED"
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_data_type(self):
        """Test validation fails with invalid data type."""
        invalid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "INVALID",
            "timestamp": "2024-04-26T10:30:00",
            "status": "COMPLETED",
            "result": {}
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "Invalid data_type" in error

    def test_validate_invalid_status(self):
        """Test validation fails with invalid status."""
        invalid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "SENSOR",
            "timestamp": "2024-04-26T10:30:00",
            "status": "INVALID",
            "result": {}
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "Invalid status" in error

    def test_validate_invalid_timestamp_format(self):
        """Test validation fails with invalid timestamp format."""
        invalid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "SENSOR",
            "timestamp": "2024/04/26 10:30:00",
            "status": "COMPLETED",
            "result": {}
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "Invalid timestamp format" in error

    def test_validate_invalid_result_type(self):
        """Test validation fails with invalid result type."""
        invalid_analysis = {
            "analysis_id": "analysis_123",
            "data_type": "SENSOR",
            "timestamp": "2024-04-26T10:30:00",
            "status": "COMPLETED",
            "result": "not a dict"
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "Result must be a dictionary" in error

    def test_validate_invalid_analysis_id(self):
        """Test validation fails with invalid analysis_id."""
        invalid_analysis = {
            "analysis_id": "",
            "data_type": "SENSOR",
            "timestamp": "2024-04-26T10:30:00",
            "status": "COMPLETED",
            "result": {}
        }
        is_valid, error = AnalysisValidator.validate_analysis(invalid_analysis)
        assert is_valid is False
        assert "analysis_id must be a non-empty" in error

    def test_validate_all_data_types_and_statuses(self):
        """Test validation with all valid data types and statuses."""
        for data_type in ["SENSOR", "LOG", "METRIC", "EVENT"]:
            for status in ["PENDING", "PROCESSING", "COMPLETED", "FAILED"]:
                analysis = {
                    "analysis_id": "analysis_123",
                    "data_type": data_type,
                    "timestamp": "2024-04-26T10:30:00",
                    "status": status,
                    "result": {"data": f"test_{data_type}_{status}"}
                }
                is_valid, error = AnalysisValidator.validate_analysis(analysis)
                assert is_valid is True, f"Data type {data_type} with status {status} should be valid"

    def test_validate_analysis_batch_all_valid(self):
        """Test batch validation with all valid analyses."""
        analyses = [
            {
                "analysis_id": "analysis_1",
                "data_type": "SENSOR",
                "timestamp": "2024-04-26T10:30:00",
                "status": "COMPLETED",
                "result": {"temperature": 25.5}
            },
            {
                "analysis_id": "analysis_2",
                "data_type": "LOG",
                "timestamp": "2024-04-26T10:31:00",
                "status": "PROCESSING",
                "result": {"entries": 100}
            }
        ]
        all_valid, errors = AnalysisValidator.validate_analysis_batch(analyses)
        assert all_valid is True
        assert errors == []

    def test_validate_analysis_batch_with_errors(self):
        """Test batch validation with some invalid analyses."""
        analyses = [
            {
                "analysis_id": "analysis_1",
                "data_type": "SENSOR",
                "timestamp": "2024-04-26T10:30:00",
                "status": "COMPLETED",
                "result": {"temperature": 25.5}
            },
            {
                "analysis_id": "",
                "data_type": "INVALID",
                "timestamp": "invalid",
                "status": "INVALID",
                "result": "not a dict"
            }
        ]
        all_valid, errors = AnalysisValidator.validate_analysis_batch(analyses)
        assert all_valid is False
        assert len(errors) == 1
        assert errors[0]["index"] == 1


class TestMetricValidator:
    """Test cases for MetricValidator class."""

    def test_validate_valid_metric(self):
        """Test validation of a valid metric."""
        valid_metric = {
            "name": "temperature",
            "value": 25.5,
            "timestamp": "2024-04-26T10:30:00",
            "unit": "celsius"
        }
        is_valid, error = MetricValidator.validate_metric(valid_metric)
        assert is_valid is True
        assert error is None

    def test_validate_missing_metric_field(self):
        """Test validation fails when required metric field is missing."""
        invalid_metric = {
            "name": "temperature",
            "value": 25.5,
            "timestamp": "2024-04-26T10:30:00"
        }
        is_valid, error = MetricValidator.validate_metric(invalid_metric)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_metric_name(self):
        """Test validation fails with invalid metric name."""
        invalid_metric = {
            "name": "",
            "value": 25.5,
            "timestamp": "2024-04-26T10:30:00",
            "unit": "celsius"
        }
        is_valid, error = MetricValidator.validate_metric(invalid_metric)
        assert is_valid is False
        assert "Metric name must be a non-empty string" in error

    def test_validate_invalid_metric_value(self):
        """Test validation fails with invalid metric value."""
        invalid_metric = {
            "name": "temperature",
            "value": "25.5",
            "timestamp": "2024-04-26T10:30:00",
            "unit": "celsius"
        }
        is_valid, error = MetricValidator.validate_metric(invalid_metric)
        assert is_valid is False
        assert "Metric value must be a number" in error

    def test_validate_invalid_metric_timestamp(self):
        """Test validation fails with invalid timestamp."""
        invalid_metric = {
            "name": "temperature",
            "value": 25.5,
            "timestamp": "invalid",
            "unit": "celsius"
        }
        is_valid, error = MetricValidator.validate_metric(invalid_metric)
        assert is_valid is False
        assert "Invalid timestamp format" in error

    def test_validate_invalid_metric_unit(self):
        """Test validation fails with invalid unit."""
        invalid_metric = {
            "name": "temperature",
            "value": 25.5,
            "timestamp": "2024-04-26T10:30:00",
            "unit": ""
        }
        is_valid, error = MetricValidator.validate_metric(invalid_metric)
        assert is_valid is False
        assert "Unit must be a non-empty string" in error

    def test_validate_metric_batch_all_valid(self):
        """Test batch validation with all valid metrics."""
        metrics = [
            {
                "name": "temperature",
                "value": 25.5,
                "timestamp": "2024-04-26T10:30:00",
                "unit": "celsius"
            },
            {
                "name": "humidity",
                "value": 60,
                "timestamp": "2024-04-26T10:31:00",
                "unit": "percent"
            }
        ]
        all_valid, errors = MetricValidator.validate_metric_batch(metrics)
        assert all_valid is True
        assert errors == []

    def test_validate_metric_batch_with_errors(self):
        """Test batch validation with some invalid metrics."""
        metrics = [
            {
                "name": "temperature",
                "value": 25.5,
                "timestamp": "2024-04-26T10:30:00",
                "unit": "celsius"
            },
            {
                "name": "",
                "value": "invalid",
                "timestamp": "invalid",
                "unit": ""
            }
        ]
        all_valid, errors = MetricValidator.validate_metric_batch(metrics)
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
            "exchange": "analysis_exchange",
            "queue": "analysis_queue"
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
            "password": "guest",
            "exchange": "analysis_exchange"
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
            "exchange": "analysis_exchange",
            "queue": "analysis_queue"
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
            "exchange": "analysis_exchange",
            "queue": "analysis_queue"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Host must be" in error

    def test_validate_valid_database_config(self):
        """Test validation of valid database configuration."""
        config = {
            "url": "sqlite:///./test_ms_analyse.db",
            "echo": False
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_database_config_key(self):
        """Test validation fails when database config key is missing."""
        config = {
            "url": "sqlite:///./test_ms_analyse.db"
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
            "url": "sqlite:///./test_ms_analyse.db",
            "echo": "yes"
        }
        is_valid, error = ConfigValidator.validate_database_config(config)
        assert is_valid is False
        assert "Echo setting must be a boolean" in error
