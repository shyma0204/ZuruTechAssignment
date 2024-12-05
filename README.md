# ZuruTechAssignment (pyls)

This project is a solution for a Python technical test where the goal is to implement a program `pyls` that mimics the behavior of the Linux `ls` command for visualizing file system structures stored in a JSON format. The program supports features such as listing files, filtering, sorting, handling paths, and displaying human-readable sizes.

## Features

- Mimics the behavior of the Linux `ls` command for listing files and directories.
- Supports options for:
  - Including hidden files (`-A`).
  - Displaying detailed file information (`-l`).
  - Sorting by time when the file was modified (`-t`) and reversing order (`-r`).
  - Filtering results by file type (`--filter=file` or `--filter=dir`).
  - Though not specifically required in the assignment, I’ve added an option `--path=json_file_location` to allow parsing a custom JSON file given its absolute location
- Supports relative paths within the root directory by specifying it as a positional argument.
- Logs execution details for debugging and analysis.

## Installation

There are two ways to install the program:

### Install as a package using `pip`:
1. Start by cloning the repository.
2. Create a virtual environment and activate it.
3. In the repository's root directory, where `pyproject.toml` is located, run the following command: `pip install .`
4. The program should now be installed. Verify the installation by running `pyls --help`.

### Run the program directly:
1. Start by cloning the repository.
2. Create a virtual environment and activate it.
3. In the repository's root directory install the required packages by running: `pip install -r requirements.txt`
4. Run the program by executing the following command: `python -m pyls --help`


## Usage
If you have installed the program as a package, you can run it using the `pyls` command. If you have run the program directly, you can run it using the `python -m pyls` command.

### Examples
- The following command lists all files (excluding directories) from the default JSON file named structure.json, located in the _**file_system_structures**_ directory inside the **_pyls_** package. It includes hidden files, displays detailed information (such as size and modification time), and sorts the results by the last modification time. 

`pyls -A -l -t --filter=file` or `python -m pyls -A -l -t --filter=file` (depending on how you installed the program)

- The following command processes the nested path parser/parser.go inside the root directory defined in the default JSON file.

`pyls -A -r -t parser/parser.go` or `python -m pyls -A -r -t parser/parser.go`

- The next command uses a custom JSON file located at /path/to/your/custom/file.json. It includes hidden files, sorts them by modification time, and reverses the order of listing

`pyls -A -r -t --path=/path/to/your/custom/file.json` or `python -m pyls -A -r -t --path=/path/to/your/custom/file.json`

_**N.B. Don't forget to activate your virtual environment before executing the commands!**_

## For Developers
### Running Tests
You can execute the tests using `pytest`. The test files are located in the pyls/tests directory.

### Logs Location
The program generates logs during execution for debugging and analysis. The location of the log file depends on how the program is run:

1. **If executed as the `pyls` command (installed via `pip`)**:
   - Logs will be located in the installed package directory. For example:
     ```
     /path/to/your/environment/env/lib/python3.10/site-packages/pyls/app.log
     ```

2. **If executed directly from the source package**:
   - Logs will be saved in the `app.log` file located in the `pyls` directory within the source project.
     ```
     /path/to/your/source/code/pyls/app.log
     ```

## Author

Ilya Shamatula (shamatulailya@gmail.com)
