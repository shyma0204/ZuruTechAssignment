import json
import sys
from datetime import datetime, timezone


def load_json_file(file_path: str) -> dict[str, any]:
    """
    Loads a JSON file and returns its parsed contents.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict[str, any]: Parsed JSON content.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def list_contents(directory: dict[str, any], include_hidden: bool = False, reverse: bool = False,
                  sort_by: str = 'name') -> list[dict[str, any]]:
    """
    Lists the contents of the given directory.

    Args:
        directory (dict[str, any]): A dictionary representing the directory.
        include_hidden (bool): Whether to include hidden files (starting with '.').
        reverse (bool): Whether to reverse the sorting order.
        sort_by (str): The key to sort by ('name' or 'time_modified').

    Returns:
        list[dict[str, any]]: Sorted list of directory contents.
    """
    contents = directory.get('contents', [])

    if not include_hidden:
        contents = [item for item in contents if not item['name'].startswith('.')]
    return sorted(contents, key=lambda x: x[sort_by], reverse=reverse)


def format_file_details(file_item: dict[str, any]) -> str:
    """
    Formats a single directory item for -l flag output.

    Args:
        file_item (dict[str, any]): The file or directory item as a dictionary.

    Returns:
        str: A formatted string with file details.
    """
    permissions = file_item.get('permissions', '-' * 10)
    size = file_item.get('size', 0)
    time_modified = datetime.fromtimestamp(file_item.get('time_modified', 0), tz=timezone.utc).strftime('%b %d %H:%M')
    name = file_item.get('name', 'UNKNOWN')
    return f"{permissions}  {size:<6}  {time_modified}  {name}"
