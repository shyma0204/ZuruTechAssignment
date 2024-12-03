import argparse
import logging
import sys

from .utils import load_json_file, filter_directory_contents, sort_directory_contents, \
    print_directory_items, get_target_item

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description='processing arguments')
    parser.add_argument('--path', type=str, help='Path to the JSON file', default='./file_system_structures/structure.json')
    parser.add_argument('-A', action='store_true', help='Include hidden files')
    parser.add_argument('-l', action='store_true', help='Show detailed file information')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the listing')
    parser.add_argument('-t', action='store_true', help='Sort by time modified')
    parser.add_argument('--filter', type=str, choices=['file', 'dir'], help="Filter the results by 'file' or 'dir'.")
    parser.add_argument('target_path', type=str, nargs='?', default='',help='Relative path to the target directory or file.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    root_directory = load_json_file(args.path)

    target_item = get_target_item(root_directory, args.target_path)

    if target_item is None:
        sys.exit("Error: Target item not found.")

    if 'contents' not in target_item:
        print_directory_items([target_item], show_detailed_info=args.l)
    else:
        directory_items_to_show = filter_directory_contents(target_item, filter_type=args.filter, include_hidden=args.A)
        directory_items_to_show = sort_directory_contents(directory_items_to_show, sort_by='time_modified' if args.t else 'name',
                                                   reverse=args.r)
        print_directory_items(directory_items_to_show, show_detailed_info=args.l)

if __name__ == '__main__':
    main()
