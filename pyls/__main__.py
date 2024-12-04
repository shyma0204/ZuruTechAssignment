import argparse
import json
import logging
import sys
import os

from .utils import load_json_file, filter_directory_contents, sort_directory_contents, \
    print_directory_items, get_target_item


pyls_package_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(pyls_package_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    default_json_path = os.path.join(pyls_package_dir, 'file_system_structures/structure.json')

    parser = argparse.ArgumentParser(description='processing arguments')
    parser.add_argument('--path', type=str, help='Path to the JSON file', default=default_json_path)
    parser.add_argument('-A', action='store_true', help='Include hidden files')
    parser.add_argument('-l', action='store_true', help='Show detailed file information')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the listing')
    parser.add_argument('-t', action='store_true', help='Sort by time modified')
    parser.add_argument('--filter', type=str, choices=['file', 'dir'], help="Filter the results by 'file' or 'dir'.")
    parser.add_argument('target_path', type=str, nargs='?', default='',help='Relative path to the target directory or file.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        root_directory = load_json_file(args.path)
    except FileNotFoundError:
        logger.error("File not found: %s", args.path)
        sys.exit("Error: The specified file was not found.")
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON: %s", args.path)
        sys.exit("Error: The JSON file is invalid or corrupted.")
    except Exception as e:
        logger.critical("Unexpected error: %s", e)
        sys.exit(f"An unexpected error occurred: {e}")

    target_item = get_target_item(root_directory, args.target_path)

    if target_item is None:
        sys.exit("Error: Target item not found.")

    # checking if the target item is a file or a directory
    if 'contents' not in target_item:
        print_directory_items([target_item], show_detailed_info=args.l)
    else:
        directory_items_to_show = filter_directory_contents(target_item, filter_type=args.filter, include_hidden=args.A)
        directory_items_to_show = sort_directory_contents(directory_items_to_show, sort_by='time_modified' if args.t else 'name',
                                                   reverse=args.r)
        print_directory_items(directory_items_to_show, show_detailed_info=args.l)

if __name__ == '__main__':
    main()
