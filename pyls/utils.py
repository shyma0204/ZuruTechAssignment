import json
import sys

def load_json_file(file_path):
    """Loads the JSON file."""
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

def list_contents(directory, include_hidden=False):
    """Lists the contents of the given directory."""
    contents = directory.get('contents', [])
    if not include_hidden:
        contents = [item for item in contents if not item['name'].startswith('.')]
    return [item['name'] for item in contents]