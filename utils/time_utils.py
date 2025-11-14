"""
Time Utilities Module
Provides Hong Kong time (UTC+8) functions for consistent timezone handling
"""

from datetime import datetime, timezone, timedelta

# Hong Kong timezone (UTC+8)
HK_TZ = timezone(timedelta(hours=8))

def get_hk_time():
    """
    Get current time in Hong Kong timezone (UTC+8)
    Returns naive datetime with HK time values for MongoDB storage
    
    MongoDB stores timezone-aware datetime as UTC, so we return naive datetime
    with HK time values to ensure correct display.
    
    Returns:
        datetime: Current Hong Kong time (naive, for MongoDB)
    """
    # Get timezone-aware HK time
    hk_time_aware = datetime.now(HK_TZ)
    # Return as naive datetime (MongoDB will store this as-is)
    return hk_time_aware.replace(tzinfo=None)

def utc_to_hk(utc_time):
    """
    Convert UTC time to Hong Kong time
    
    Args:
        utc_time (datetime): UTC datetime object
        
    Returns:
        datetime: Hong Kong time
    """
    if utc_time is None:
        return None
    
    # If the datetime is naive (no timezone info), assume it's UTC
    if utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=timezone.utc)
    
    return utc_time.astimezone(HK_TZ)

def hk_to_utc(hk_time):
    """
    Convert Hong Kong time to UTC
    
    Args:
        hk_time (datetime): Hong Kong datetime object
        
    Returns:
        datetime: UTC time
    """
    if hk_time is None:
        return None
    
    # If the datetime is naive, assume it's HK time
    if hk_time.tzinfo is None:
        hk_time = hk_time.replace(tzinfo=HK_TZ)
    
    return hk_time.astimezone(timezone.utc)

def format_hk_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime in Hong Kong timezone
    
    Args:
        dt (datetime): Datetime object
        format_str (str): Format string
        
    Returns:
        str: Formatted time string in HK timezone
    """
    if dt is None:
        return 'N/A'
    
    hk_time = utc_to_hk(dt) if dt.tzinfo is None or dt.tzinfo.utcoffset(dt).total_seconds() == 0 else dt
    return hk_time.strftime(format_str)
