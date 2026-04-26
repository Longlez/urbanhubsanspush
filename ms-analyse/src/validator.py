"""
Validator module for ms-analyse.

This module provides validation utilities for analysis data and system configuration.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime


class AnalysisValidator:
    """Validates analysis entries according to defined rules."""

    REQUIRED_FIELDS = ["analysis_id", "data_type", "timestamp", "status", "result"]
    VALID_DATA_TYPES = ["SENSOR", "LOG", "METRIC", "EVENT"]
    VALID_STATUSES = ["PENDING", "PROCESSING", "COMPLETED", "FAILED"]

    @classmethod
    def validate_analysis(cls, analysis_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate an analysis entry.

        Args:
            analysis_data: Dictionary containing analysis entry data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in analysis_data:
                return False, f"Missing required field: {field}"

        # Validate analysis_id
        if not isinstance(analysis_data.get("analysis_id"), (int, str)) or not analysis_data["analysis_id"]:
            return False, "analysis_id must be a non-empty integer or string"

        # Validate data_type
        if analysis_data["data_type"] not in cls.VALID_DATA_TYPES:
            return False, f"Invalid data_type: {analysis_data['data_type']}. Must be one of {cls.VALID_DATA_TYPES}"

        # Validate status
        if analysis_data["status"] not in cls.VALID_STATUSES:
            return False, f"Invalid status: {analysis_data['status']}. Must be one of {cls.VALID_STATUSES}"

        # Validate timestamp format
        try:
            datetime.fromisoformat(analysis_data["timestamp"])
        except (ValueError, TypeError):
            return False, "Invalid timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Validate result is a dictionary
        if not isinstance(analysis_data.get("result"), dict):
            return False, "Result must be a dictionary"

        return True, None

    @classmethod
    def validate_analysis_batch(cls, analyses: list) -> tuple[bool, list]:
        """
        Validate a batch of analysis entries.

        Args:
            analyses: List of analysis entry dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, analysis in enumerate(analyses):
            is_valid, error_msg = cls.validate_analysis(analysis)
            if not is_valid:
                errors.append({"index": idx, "error": error_msg})

        return len(errors) == 0, errors


class MetricValidator:
    """Validates metric data."""

    REQUIRED_METRIC_FIELDS = ["name", "value", "timestamp", "unit"]

    @classmethod
    def validate_metric(cls, metric_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate a metric entry.

        Args:
            metric_data: Dictionary containing metric data

        Returns:
            Tuple of (is_valid, error_message)
        """
        for field in cls.REQUIRED_METRIC_FIELDS:
            if field not in metric_data:
                return False, f"Missing required field: {field}"

        # Validate name
        if not isinstance(metric_data.get("name"), str) or not metric_data["name"]:
            return False, "Metric name must be a non-empty string"

        # Validate value is numeric
        if not isinstance(metric_data.get("value"), (int, float)):
            return False, "Metric value must be a number"

        # Validate timestamp
        try:
            datetime.fromisoformat(metric_data["timestamp"])
        except (ValueError, TypeError):
            return False, "Invalid timestamp format. Expected ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Validate unit
        if not isinstance(metric_data.get("unit"), str) or not metric_data["unit"]:
            return False, "Unit must be a non-empty string"

        return True, None

    @classmethod
    def validate_metric_batch(cls, metrics: list) -> tuple[bool, list]:
        """
        Validate a batch of metric entries.

        Args:
            metrics: List of metric dictionaries

        Returns:
            Tuple of (all_valid, list_of_errors)
        """
        errors = []
        for idx, metric in enumerate(metrics):
            is_valid, error_msg = cls.validate_metric(metric)
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
        required_keys = ["host", "port", "username", "password", "exchange", "queue"]

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
