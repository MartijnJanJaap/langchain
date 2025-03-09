# filename: gitignore_filter.py
import os

class GitignoreFilter:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        self.gitignore_patterns = self._read_gitignore()

    def _read_gitignore(self):
        """Read and parse the .gitignore file."""
        gitignore_path = os.path.join(self.workspace_dir, '.gitignore')
        if not os.path.isfile(gitignore_path):
            return []

        with open(gitignore_path, 'r', encoding='utf-8') as file:
            # Read lines, strip whitespace, and remove comments and empty lines.
            patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return patterns

    def is_ignored(self, path):
        """Check if a given path should be ignored based on .gitignore patterns."""
        for pattern in self.gitignore_patterns:
            if self._match_pattern(path, pattern):
                return True
        # Ignore __pycache__ by default
        if '__pycache__' in path:
            return True
        return False

    def _match_pattern(self, path, pattern):
        """Match a path against a .gitignore pattern."""
        # This is a simple example. More complex pattern matching can be added.
        if pattern in path:  # Simple substring check
            return True
        return False

# Example usage:
if __name__ == '__main__':
    workspace_dir = r"C:\projects\portfoliomanager\prompt_generator\workspace"
    filter_util = GitignoreFilter(workspace_dir)
    test_path = 'example/__pycache__/file.py'
    print(f"Is '{test_path}' ignored? {filter_util.is_ignored(test_path)}")