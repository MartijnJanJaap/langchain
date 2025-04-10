# filename: file_filter.py
import os

class FileFilter:
    def __init__(self):
        # Define a list of folders/files to ignore
        self.ignore_list = [
            '__pycache__',
            'node_modules',
            '.DS_Store',
            'Thumbs.db',
            '.git',
            '.svn',
            '.vscode',
            'venv',
            '.env',
            '.angular'
        ]

    def is_ignored(self, path):
        """Checks if the path should be ignored based on predefined patterns."""
        for pattern in self.ignore_list:
            if pattern in os.path.basename(path):
                return True
        return False