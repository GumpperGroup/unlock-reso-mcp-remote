"""Logging configuration for UnlockRESO MCP Server."""

import logging
import sys
from typing import Optional

from .settings import settings


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        name: Logger name. If None, returns root logger.
    
    Returns:
        Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level_numeric)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level_numeric)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


# Create default logger for the package
default_logger = setup_logging("unlock_reso_mcp")