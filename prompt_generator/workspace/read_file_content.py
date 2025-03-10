def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="ISO-8859-1") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="windows-1252") as f:
                    return f.read()
            except Exception as e:
                print(f"[ERROR] Failed to read file '{file_path}': {e}")
                return f"(Error reading file: {e})"
    except Exception as e:
        print(f"[ERROR] Unexpected error reading file '{file_path}': {e}")
        return f"(Error reading file: {e})"
