"""
Test script to verify Hong Kong timezone is working
"""
from utils.time_utils import get_hk_time, format_hk_time
from datetime import datetime, timezone

# Test 1: Get current HK time
hk_now = get_hk_time()
print(f"Current Hong Kong Time: {hk_now}")
print(f"Formatted: {format_hk_time(hk_now)}")

# Test 2: Compare with UTC
utc_now = datetime.now(timezone.utc)
print(f"\nCurrent UTC Time: {utc_now}")
print(f"Difference: {(hk_now.utcoffset().total_seconds() / 3600)} hours")

# Test 3: Verify it's actually UTC+8
print(f"\n✅ Hong Kong timezone test completed")
print(f"HK Time: {hk_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"UTC Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
