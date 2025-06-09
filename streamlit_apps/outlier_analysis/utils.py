from decimal import ROUND_HALF_UP, Decimal

import pandas as pd


def safe_extract(series, default=0, as_type=float):
    """Safely extract first item from a Series and convert to given type."""
    if isinstance(series, pd.Series) and not series.empty and pd.notna(series.iloc[0]):
        return as_type(series.iloc[0])
    return default

def round_nearest_int(value):
    """Round a value to the nearest integer, converting Decimal to int if necessary."""
    if not isinstance(value, Decimal):
        value = Decimal(value)
    converted_value = int((value).to_integral_value(rounding=ROUND_HALF_UP))
    return f"{converted_value:,}" 

def format_large_number(value):
    """Format large numbers with commas and add $ as prefix."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value:.2f}"