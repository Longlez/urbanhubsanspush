"""
Unit tests for the validator module.
"""

import pytest
from datetime import datetime
from src.validator import SensorDataValidator, DeviceValidator, ConfigValidator


class TestSensorDataValidator:
    """Test cases for SensorDataValidator class."""

    def test_validate_valid_sensor_data(self):
        """Test validation of valid sensor data."""
        valid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5, "unit": "celsius"},
            "location": {"latitude": 45.5017, "longitude": -73.5673}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(valid_sensor_data)
        assert is_valid is True
        assert error is None

    def test_validate_missing_required_field(self):
        """Test validation fails when required field is missing."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_device_type(self):
        """Test validation fails with invalid device type."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "INVALID",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5},
            "location": {"latitude": 45.5017, "longitude": -73.5673}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Invalid device_type" in error

    def test_validate_invalid_timestamp_format(self):
        """Test validation fails with invalid timestamp format."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024/04/26 10:30:00",
            "data": {"temperature": 25.5},
            "location": {"latitude": 45.5017, "longitude": -73.5673}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Invalid timestamp format" in error

    def test_validate_invalid_data_type(self):
        """Test validation fails with invalid data type."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": "not a dict",
            "location": {"latitude": 45.5017, "longitude": -73.5673}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Data must be a dictionary" in error

    def test_validate_invalid_location(self):
        """Test validation fails with invalid location."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5},
            "location": {"latitude": 45.5017}  # missing longitude
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Location must be a dictionary" in error

    def test_validate_invalid_coordinates(self):
        """Test validation fails with invalid coordinates."""
        invalid_sensor_data = {
            "sensor_id": "temp_sensor_001",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5},
            "location": {"latitude": 91, "longitude": -73.5673}  # invalid latitude
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "Latitude must be between" in error

    def test_validate_invalid_sensor_id(self):
        """Test validation fails with invalid sensor_id."""
        invalid_sensor_data = {
            "sensor_id": "",
            "device_type": "TEMPERATURE",
            "timestamp": "2024-04-26T10:30:00",
            "data": {"temperature": 25.5},
            "location": {"latitude": 45.5017, "longitude": -73.5673}
        }
        is_valid, error = SensorDataValidator.validate_sensor_data(invalid_sensor_data)
        assert is_valid is False
        assert "sensor_id must be a non-empty" in error

    def test_validate_all_device_types(self):
        """Test validation with all valid device types."""
        for device_type in ["TEMPERATURE", "HUMIDITY", "PRESSURE", "MOTION", "LIGHT", "GPS"]:
            sensor_data = {
                "sensor_id": "sensor_001",
                "device_type": device_type,
                "timestamp": "2024-04-26T10:30:00",
                "data": {"value": 25.5},
                "location": {"latitude": 45.5017, "longitude": -73.5673}
            }
            is_valid, error = SensorDataValidator.validate_sensor_data(sensor_data)
            assert is_valid is True, f"Device type {device_type} should be valid"

    def test_validate_sensor_data_batch_all_valid(self):
        """Test batch validation with all valid sensor data."""
        sensor_data_list = [
            {
                "sensor_id": "temp_sensor_001",
                "device_type": "TEMPERATURE",
                "timestamp": "2024-04-26T10:30:00",
                "data": {"temperature": 25.5},
                "location": {"latitude": 45.5017, "longitude": -73.5673}
            },
            {
                "sensor_id": "humidity_sensor_002",
                "device_type": "HUMIDITY",
                "timestamp": "2024-04-26T10:31:00",
                "data": {"humidity": 60},
                "location": {"latitude": 45.5017, "longitude": -73.5673}
            }
        ]
        all_valid, errors = SensorDataValidator.validate_sensor_data_batch(sensor_data_list)
        assert all_valid is True
        assert errors == []

    def test_validate_sensor_data_batch_with_errors(self):
        """Test batch validation with some invalid sensor data."""
        sensor_data_list = [
            {
                "sensor_id": "temp_sensor_001",
                "device_type": "TEMPERATURE",
                "timestamp": "2024-04-26T10:30:00",
                "data": {"temperature": 25.5},
                "location": {"latitude": 45.5017, "longitude": -73.5673}
            },
            {
                "sensor_id": "",
                "device_type": "INVALID",
                "timestamp": "invalid",
                "data": "not a dict",
                "location": {"latitude": 91, "longitude": 200}
            }
        ]
        all_valid, errors = SensorDataValidator.validate_sensor_data_batch(sensor_data_list)
        assert all_valid is False
        assert len(errors) == 1
        assert errors[0]["index"] == 1


class TestDeviceValidator:
    """Test cases for DeviceValidator class."""

    def test_validate_valid_device(self):
        """Test validation of a valid device."""
        valid_device = {
            "device_id": "device_001",
            "device_type": "TEMPERATURE",
            "status": "ACTIVE",
            "last_seen": "2024-04-26T10:30:00"
        }
        is_valid, error = DeviceValidator.validate_device(valid_device)
        assert is_valid is True
        assert error is None

    def test_validate_missing_device_field(self):
        """Test validation fails when required device field is missing."""
        invalid_device = {
            "device_id": "device_001",
            "device_type": "TEMPERATURE",
            "status": "ACTIVE"
        }
        is_valid, error = DeviceValidator.validate_device(invalid_device)
        assert is_valid is False
        assert "Missing required field" in error

    def test_validate_invalid_device_status(self):
        """Test validation fails with invalid device status."""
        invalid_device = {
            "device_id": "device_001",
            "device_type": "TEMPERATURE",
            "status": "INVALID",
            "last_seen": "2024-04-26T10:30:00"
        }
        is_valid, error = DeviceValidator.validate_device(invalid_device)
        assert is_valid is False
        assert "Status must be one of" in error

    def test_validate_invalid_device_id(self):
        """Test validation fails with invalid device_id."""
        invalid_device = {
            "device_id": "",
            "device_type": "TEMPERATURE",
            "status": "ACTIVE",
            "last_seen": "2024-04-26T10:30:00"
        }
        is_valid, error = DeviceValidator.validate_device(invalid_device)
        assert is_valid is False
        assert "device_id must be a non-empty" in error

    def test_validate_invalid_device_timestamp(self):
        """Test validation fails with invalid last_seen timestamp."""
        invalid_device = {
            "device_id": "device_001",
            "device_type": "TEMPERATURE",
            "status": "ACTIVE",
            "last_seen": "invalid"
        }
        is_valid, error = DeviceValidator.validate_device(invalid_device)
        assert is_valid is False
        assert "Invalid last_seen timestamp format" in error

    def test_validate_device_batch_all_valid(self):
        """Test batch validation with all valid devices."""
        devices = [
            {
                "device_id": "device_001",
                "device_type": "TEMPERATURE",
                "status": "ACTIVE",
                "last_seen": "2024-04-26T10:30:00"
            },
            {
                "device_id": "device_002",
                "device_type": "HUMIDITY",
                "status": "INACTIVE",
                "last_seen": "2024-04-26T10:31:00"
            }
        ]
        all_valid, errors = DeviceValidator.validate_device_batch(devices)
        assert all_valid is True
        assert errors == []

    def test_validate_device_batch_with_errors(self):
        """Test batch validation with some invalid devices."""
        devices = [
            {
                "device_id": "device_001",
                "device_type": "TEMPERATURE",
                "status": "ACTIVE",
                "last_seen": "2024-04-26T10:30:00"
            },
            {
                "device_id": "",
                "device_type": "INVALID",
                "status": "INVALID",
                "last_seen": "invalid"
            }
        ]
        all_valid, errors = DeviceValidator.validate_device_batch(devices)
        assert all_valid is False
        assert len(errors) == 1
        assert errors[0]["index"] == 1


class TestConfigValidator:
    """Test cases for ConfigValidator class."""

    def test_validate_valid_mongodb_config(self):
        """Test validation of valid MongoDB configuration."""
        config = {
            "host": "localhost",
            "port": 27017,
            "database": "iot_data",
            "username": "iot_user",
            "password": "iot_password"
        }
        is_valid, error = ConfigValidator.validate_mongodb_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_mongodb_config_key(self):
        """Test validation fails when MongoDB config key is missing."""
        config = {
            "host": "localhost",
            "port": 27017,
            "database": "iot_data",
            "username": "iot_user"
        }
        is_valid, error = ConfigValidator.validate_mongodb_config(config)
        assert is_valid is False
        assert "Missing required configuration key" in error

    def test_validate_invalid_mongodb_port(self):
        """Test validation fails with invalid MongoDB port."""
        config = {
            "host": "localhost",
            "port": 99999,
            "database": "iot_data",
            "username": "iot_user",
            "password": "iot_password"
        }
        is_valid, error = ConfigValidator.validate_mongodb_config(config)
        assert is_valid is False
        assert "Port must be" in error

    def test_validate_empty_mongodb_host(self):
        """Test validation fails with empty MongoDB host."""
        config = {
            "host": "",
            "port": 27017,
            "database": "iot_data",
            "username": "iot_user",
            "password": "iot_password"
        }
        is_valid, error = ConfigValidator.validate_mongodb_config(config)
        assert is_valid is False
        assert "Host must be" in error

    def test_validate_valid_rabbitmq_config(self):
        """Test validation of valid RabbitMQ configuration."""
        config = {
            "host": "localhost",
            "port": 5672,
            "username": "guest",
            "password": "guest",
            "exchange": "iot_exchange",
            "queue": "sensor_data_queue"
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
            "exchange": "iot_exchange"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Missing required configuration key" in error

    def test_validate_invalid_rabbitmq_port(self):
        """Test validation fails with invalid RabbitMQ port."""
        config = {
            "host": "localhost",
            "port": 99999,
            "username": "guest",
            "password": "guest",
            "exchange": "iot_exchange",
            "queue": "sensor_data_queue"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Port must be" in error

    def test_validate_empty_rabbitmq_host(self):
        """Test validation fails with empty RabbitMQ host."""
        config = {
            "host": "",
            "port": 5672,
            "username": "guest",
            "password": "guest",
            "exchange": "iot_exchange",
            "queue": "sensor_data_queue"
        }
        is_valid, error = ConfigValidator.validate_rabbitmq_config(config)
        assert is_valid is False
        assert "Host must be" in error
