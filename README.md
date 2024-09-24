# xtaskill

xtaskill is a simple command-line utility for managing windows and processes on Windows operating systems. It allows users to close a window by clicking on it or terminate the associated process. The utility is built using Python and utilizes Windows API calls to achieve its functionality.

## Features

- **Closes a Window**: Click on any window to close it using its window handle.
- **Terminate a Process**: Click on any window to retrieve its process ID and terminate the associated process.
- **Command-line Arguments**: Specify behavior using command-line options.

## Installation

1. Download the `xtaskill.exe` file from the [releases](link-to-releases) section.
2. Place the executable in a directory included in your system's PATH, or use it directly from its location.

## Usage

You can use `xtaskill.exe` from the command line as follows:

### To Close a Window

Set up the hook to capture the window handle and close the window when clicked:

```bash
xtaskill.exe -win
```

### To Terminate a Process
Set up the hook to capture the process ID and terminate the process when clicked:

```bash
xtaskill.exe
```

## Requirements
Windows operating system
No external libraries are required, as it uses built-in Windows API calls through Python's ctypes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any changes or improvements.

## Acknowledgments
Thanks to the Python community and the maintainers of the Windows API for their valuable resources and documentation.
