"""This module can also be executed as a Command Line utility."""

import sys

if __name__ == '__main__':
    import pyJsJson
    success = pyJsJson.main.main(sys.argv[1:])
    if not success:
        sys.exit(1)