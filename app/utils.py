"""Utility functions for data validation and generation.

This module provides validation and generation utilities for the application,
including VIN number generation and various data validators.
"""
import random
import string
from datetime import datetime, timezone, date as date_type


def generate_chasis_number() -> str:
    """Generate a random VIN (Vehicle Identification Number).
    
    Returns:
        str: A 17-character VIN following the standard format.
    """
    # Exclude I, O, Q as per VIN standards
    chars = (
        string.ascii_uppercase.replace("I", "").replace("O", "").replace("Q", "")
        + string.digits
    )
    return "".join(random.choice(chars) for _ in range(17))


def is_valid_year(year: int) -> bool:
    """Validate that the vehicle year is within acceptable range.
    
    Args:
        year: The year to validate.
        
    Returns:
        bool: True if year is between 1900 and current year, False otherwise.
    """
    current_year = datetime.now().year
    return 1900 <= year <= current_year


def is_valid_price(price: float) -> bool:
    """Validate that the price is greater than zero.
    
    Args:
        price: The price to validate.
        
    Returns:
        bool: True if price is greater than 0, False otherwise.
    """
    return price > 0


def is_valid_future_date(date: datetime) -> bool:
    """Validate that the provided date is not in the future.
    
    Args:
        date: The datetime object to validate.
        
    Returns:
        bool: True if date is today or in the past, False if in the future.
    """
    today = (
        datetime.now(timezone.utc).date()
        if date.tzinfo
        else datetime.now().date()
    )

    if date.tzinfo:
        date_only = date.astimezone(timezone.utc).date()
    else:
        date_only = date.date()

    return date_only <= today


def is_valid_comprador_name(nombre: str) -> bool:
    """Validate that the buyer name is not empty.
    
    Args:
        nombre: The buyer name to validate.
        
    Returns:
        bool: True if name is not empty and has content, False otherwise.
    """
    return bool(nombre and nombre.strip())
