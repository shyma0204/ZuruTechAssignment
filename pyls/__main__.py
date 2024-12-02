import sys
import argparse
from .utils import load_json_file, list_contents, format_file_details


def main():
    parser = argparse.ArgumentParser(description='processing arguments')

    parser.add_argument('--path', type=str, help='Path to the json file', default='./structure.json')
    parser.add_argument('-A', action='store_true', help='Include hidden files ')
    parser.add_argument('-l', action='store_true', help='Show detailed file information')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the listing')
    parser.add_argument('-t', action='store_true', help='Sort by time modified')

    args = parser.parse_args()

    # print(f"Using JSON structure path: {args.path}")
    directory_structure = load_json_file(args.path)

    directory_items_to_show = list_contents(directory_structure, include_hidden=args.A, reverse=args.r,
                                            sort_by='time_modified' if args.t else 'name')

    if args.l:
        for item in directory_items_to_show:
            print(format_file_details(item))
    else:
        print(" ".join([item['name'] for item in directory_items_to_show]))

if __name__ == '__main__':
    main()
