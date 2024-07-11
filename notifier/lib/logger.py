"""
Module for storing logger object and settings
"""

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
