"""
Module for loading configuration from a JSON file.
"""

import json
from typing import Any, Dict
from pathlib import Path


def load_config(path: Path) -> Dict[str, Any]:
    """
    Load a configuration from a JSON file.

    Args:
        path (str): The path to the JSON file to be loaded.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed JSON data.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)