"""
Validator module for ms-collecte-iot.

This module provides validation utilities for IoT sensor data and system configuration.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime


class SensorDataValidator:
    """Validates IoT sensor data entries according to defined rules."""

    REQUIRED_FIELDS = ["sensor_id", "device_type", "timestamp", "data", "location"]
    VALID_DEVICE_TYPES = ["TEMPERATURE", "HUMIDITY", "PRESSURE", "MOTION", "LIGHT", "GPS"]

    @classmethod
    def validate_sensor_data(cls, sensor_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate a sensor data entry.

        Args:
            sensor_data: Dictionary containing sensor data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in sensor_data:
                return False, f"Missing required field: {field}"

        # Validate sensor_id
        if not isinstance(sensor_data.get("sensor_id"), (int, str)) or not sensor_data["sensor_id"]:
            return False, "sensor_id must be a non-empty integer or string"

        # Validate device_type
        if sensor_data["device_type"] not in cls.VALID_DEVICE_TYPES:
            return False, f"Invalid device_type: {sensor_data['device_type']}. Must be one of {cls.VALID_DEVICE_TYPES}"

        # Validate timestamp format
        try:
            datetime.fromisoformat(sensor_data["timestamp"])
        except (ValueError, TypeError):
            return False, "Invalid timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Validate data is a dictionary
        if not isinstance(sensor_data.get("data"), dict):
            return False, "Data must be a dictionary"

        # Validate location
        location = sensor_data.get("location")
        if not isinstance(location, dict) or not location.get("latitude") or not location.get("longitude"):
            return False, "Location must be a dictionary with latitude and longitude"

        # Validate coordinates
        try:
            lat = float(location["latitude"])
            lon = float(location["longitude"])
            if not (-90 <= lat <= 90):
                return False, "Latitude must be between -90 and 90"
            if not (-180 <= lon <= 180):
                return False, "Longitude must be between -180 and 180"
        except (ValueError, TypeError):
            return False, "Latitude and longitude must be valid numbers"

        return True, None

    @classmethod
    def validate_sensor_data_batch(cls, sensor_data_list: list) -> tuple[bool, list]:
        """
        Validate a batch of sensor data entries.

        Args:
            sensor_data_list: List of sensor data dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, sensor_data in enumerate(sensor_data_list):
            is_valid, error_msg = cls.validate_sensor_data(sensor_data)
            if not is_valid:
                errors.append({"index": idx, "error": error_msg})

        return len(errors) == 0, errors


class DeviceValidator:
    """Validates IoT device configurations."""

    REQUIRED_DEVICE_FIELDS = ["device_id", "device_type", "status", "last_seen"]

    @classmethod
    def validate_device(cls, device_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate a device entry.

        Args:
            device_data: Dictionary containing device data

        Returns:
            Tuple of (is_valid, error_message)
        """
        for field in cls.REQUIRED_DEVICE_FIELDS:
            if field not in device_data:
                return False, f"Missing required field: {field}"

        # Validate device_id
        if not isinstance(device_data.get("device_id"), (int, str)) or not device_data["device_id"]:
            return False, "device_id must be a non-empty integer or string"

        # Validate device_type
        if device_data["device_type"] not in SensorDataValidator.VALID_DEVICE_TYPES:
            return False, f"Invalid device_type: {device_data['device_type']}. Must be one of {SensorDataValidator.VALID_DEVICE_TYPES}"

        # Validate status
        if device_data["status"] not in ["ACTIVE", "INACTIVE", "MAINTENANCE", "OFFLINE"]:
            return False, "Status must be one of: ACTIVE, INACTIVE, MAINTENANCE, OFFLINE"

        # Validate last_seen timestamp
        try:
            datetime.fromisoformat(device_data["last_seen"])
        except (ValueError, TypeError):
            return False, "Invalid last_seen timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        return True, None

    @classmethod
    def validate_device_batch(cls, devices: list) -> tuple[bool, list]:
        """
        Validate a batch of device entries.

        Args:
            devices: List of device dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, device in enumerate(devices):
            is_valid, error_msg = cls.validate_device(device)
            if not is_valid:
                errors.append({"index": idx, "error": error_msg})

        return len(errors) == 0, errors


class ConfigValidator:
    """Validates system configuration."""

    @classmethod
    def validate_mongodb_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate MongoDB configuration.

        Args:
            config: Dictionary containing MongoDB configuration

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

    @classmethod
    def validate_rabbitmq_config(cls, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate RabbitMQ configuration.

        Args:
            config: Dictionary containing RabbitMQ configuration

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ["host", "port", "username", "password", "exchange", "queue"]

        for key in required_keys:
            if key not in config:
                return False, f"Missing required configuration key: {key}"

        if not isinstance(config.get("port"), int) or not (0 < config["port"] < 65536):
            return False, "Port must be an integer between 1 and 65535"

        if not config.get("host"):
            return False, "Host must be a non-empty string"

        return True, None
