import sys
import argparse
from .utils import load_json_file, list_contents


def main():
    parser = argparse.ArgumentParser(description='processing arguments')
    parser.add_argument(
        '--path',
        type=str,
        help='path to the json structure',
        default='./structure.json'
    )

    parser.add_argument(
        '-A',
        action='store_true',
        help='Include hidden files '
    )

    args = parser.parse_args()

    # print(f"Using JSON structure path: {args.path}")
    directory_structure = load_json_file(args.path)

    visible_items = list_contents(directory_structure, include_hidden=args.A)
    print(" ".join(visible_items))

if __name__ == '__main__':
    main()
