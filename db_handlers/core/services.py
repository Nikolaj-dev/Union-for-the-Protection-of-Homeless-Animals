from datetime import datetime
from enum import Enum


async def retrieve_attributes(obj):
    """
    Retrieve all attributes of an object, excluding internal attributes starting with '_'.

    Args:
        obj: The object whose attributes need to be retrieved.

    Returns:
        dict: A dictionary containing user-defined attributes.
    """
    obj_attributes = obj.__dict__

    # Convert enum values to string
    formatted_attributes = {
        key: value.value if isinstance(value, Enum) else (
            value.strftime("%Y-%m-%d %I:%M %p") if isinstance(value, datetime) else value
        )
        for key, value in obj_attributes.items() if not key.startswith('_')
    }

    return formatted_attributes


async def row_to_dict(result):
    """
    Convert rows from a ResultProxy to a list of dictionaries.

    Args:
        result: SQLAlchemy ResultProxy.

    Returns:
        list: A list of dictionaries, each representing a row.
    """
    column_names = result.keys()
    records = result.fetchall()

    # Convert datetime objects and Enum values to formatted strings
    formatted_records = []
    for record in records:
        formatted_record = {
            key: value.value if isinstance(value, Enum) else (
                value.strftime("%Y-%m-%d %I:%M %p") if isinstance(value, datetime) else value
            )
            for key, value in zip(column_names, record)
        }
        formatted_records.append(formatted_record)

    return formatted_records

