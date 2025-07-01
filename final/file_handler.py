import json

def load_students(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error reading file. Starting with empty student list.")
        return []

def save_students(students, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save file: {e}")
