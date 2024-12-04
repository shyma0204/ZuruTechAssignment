import json
from datetime import datetime, timezone
import  logging
from typing import Optional

logger = logging.getLogger(__name__)


def load_json_file(file_path: str) -> dict[str, any]:
    """
    Loads a JSON file and returns its parsed contents.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict[str, any]: Parsed JSON content.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        logger.info("JSON file loaded successfully: %s", file_path)
        return data


def sort_directory_contents(directory_items: list[dict[str, any]], sort_by: str = 'name', reverse: bool = False) -> \
        list[dict[str, any]]:
    """
    Sorts a list of directory items by a given key and optionally reverses the order.

    Args:
        directory_items (list[dict[str, any]]): List of directory items to sort.
        sort_by (str): The key to sort by ('name' or 'time_modified').
        reverse (bool): Whether to reverse the sorting order.

    Returns:
        list[dict[str, any]]: Sorted list of directory items.

    """

    logger.info("Sorting directory items by %s, reverse=%s", sort_by, reverse)

    try:
        return sorted(directory_items, key=lambda x: x[sort_by], reverse=reverse)
    except KeyError as e:
        logger.error("Sorting failed. Missing key: %s", e)
        raise


def print_directory_items(directory_items: list[dict[str, any]], show_detailed_info: bool = False) -> None:
    """
    Prints a list of directory items with optional detailed information.

    Args:
        directory_items (list[dict[str, any]]): List of directory items to print.
        show_detailed_info (bool): Whether to show detailed information.
    """
    logger.info("Printing directory items. Detailed info: %s", show_detailed_info)

    if show_detailed_info:
        for item in directory_items:
            print(format_file_details(item))
    else:
        print(" ".join([item.get('name','UNKNOWN') for item in directory_items]))


def filter_directory_contents(directory: dict[str, any], filter_type: str = None,
                              include_hidden: bool = False) -> list[dict[str, any]]:
    """
    Filters a given directory content by type ('file' or 'dir') and optionally includes hidden files.

    Args:
        directory (dict[str, any]): A dictionary representing the directory.
        filter_type (str): The type to filter by ('file' or 'dir').
        include_hidden (bool): Whether to include hidden files (starting with '.').

    Returns:
        list[dict[str, any]]: Filtered list of directory contents.
    """
    logger.info("Filtering directory contents. Filter: %s, Include hidden: %s", filter_type, include_hidden)

    contents = directory.get('contents', [])


    if not include_hidden:
        contents = [item for item in contents if item.get('name') and not item['name'].startswith('.')]

    if filter_type:
        if filter_type == 'file':
            contents = [item for item in contents if 'contents' not in item]
        elif filter_type == 'dir':
            contents = [item for item in contents if 'contents' in item]

    return contents


def format_file_details(file_item: dict[str, any]) -> str:
    """
    Formats a single directory item for -l flag output.

    Args:
        file_item (dict[str, any]): The file or directory item as a dictionary.

    Returns:
        str: A formatted string with file or directory details.
    """
    permissions = file_item.get('permissions', '-' * 10)
    size = human_readable_size(file_item.get('size', 0))
    time_modified = datetime.fromtimestamp(file_item.get('time_modified', 0), tz=timezone.utc).strftime('%b %d %H:%M')
    name = file_item.get('name', 'UNKNOWN')
    return f"{permissions}  {size:<6}  {time_modified}  {name}"


def get_target_item(root_directory: dict[str, any], target_path: str) -> Optional[dict[str, any]]:
    """
    Retrieves the target file or directory from the root directory based on the provided path.

    Args:
        root_directory (dict[str, any]): The root directory structure.
        target_path (str): The relative path to the target item.

    Returns:
        Optional[dict[str, any]]: The target item if found, otherwise None.
    """
    try:
        if not target_path:
            return root_directory

        parts = target_path.split('/')
        current = root_directory
        for part in parts:
            if 'contents' in current:
                current = next((item for item in current['contents'] if item.get('name') and item['name'] == part), None)
            else:
                raise KeyError(f"Path '{target_path}' does not exist.")
            if current is None:
                raise KeyError(f"Path '{target_path}' does not exist.")
        return current

    except KeyError as e:
        logger.warning("Invalid path provided: %s", e)
        return None


def human_readable_size(size: int) -> str:
    """
    Converts a file size in bytes to a human-readable string.

    Args:
        size (int): File size in bytes.

    Returns:
        str: Human-readable file size.

    Raises:
    TypeError: If the size is not an integer.
    ValueError: If the size is negative.
    """

    if not isinstance(size, int):
        raise TypeError("Size must be an integer.")
    if size < 0:
        raise ValueError("Size must not be negative.")

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"