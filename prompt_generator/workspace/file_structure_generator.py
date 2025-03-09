# filename: file_structure_generator.py
import os

from prompt_generator.workspace.gitignore_filter import GitignoreFilter

class FileStructureGenerator:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        self.gitignore_filter = GitignoreFilter(workspace_dir)

    def get_file_structure_string(self):
        """Recursively build the file structure as a string."""
        return self._build_structure(self.workspace_dir)

    def _build_structure(self, directory):
        file_structure = []
        for dirpath, dirnames, filenames in os.walk(directory):
            if self.gitignore_filter.is_ignored(dirpath):
                continue

            level = dirpath.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            file_structure.append(f"{indent}{os.path.basename(dirpath)}/")

            for dirname in list(dirnames):  # Convert to list to safely modify during iteration
                full_path = os.path.join(dirpath, dirname)
                if self.gitignore_filter.is_ignored(full_path):
                    dirnames.remove(dirname)  # Modify in-place to prevent os.walk from visiting

            subindent = ' ' * 4 * (level + 1)
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                if self.gitignore_filter.is_ignored(full_path):
                    continue
                file_structure.append(f"{subindent}{filename}")
        return "\n".join(file_structure)

# Example usage:
if __name__ == '__main__':
    workspace_dir = r"C:\projects\portfoliomanager\prompt_generator\workspace"
    generator = FileStructureGenerator(workspace_dir)
    structure_string = generator.get_file_structure_string()
    print("Filtered File Structure:\n", structure_string)