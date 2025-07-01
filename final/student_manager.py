import uuid
from utils import generate_id

class StudentManager:
    def __init__(self, students=None):
        self.students = students if students else []

    def add_student(self):
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        address = input("Enter address (optional): ").strip()
        
        try:
            grade = float(input("Enter grade (0-100): ").strip())
        except ValueError:
            print("Invalid grade. Please enter a number.")
            return

        student = {
            "id": generate_id(),
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "grade": grade
        }

        self.students.append(student)
        print("Student added successfully!")

    def display_students(self):
        if not self.students:
            print("No students found.")
            return

        print("\nSort by:")
        print("1. First name (asc)")
        print("2. First name (desc)")
        print("3. Last name (asc)")
        print("4. Last name (desc)")
        print("5. Grade (asc)")
        print("6. Grade (desc)")
        choice = input("Choose an option (1-6): ")

        key_map = {
            "1": ("first_name", False),
            "2": ("first_name", True),
            "3": ("last_name", False),
            "4": ("last_name", True),
            "5": ("grade", False),
            "6": ("grade", True),
        }

        if choice in key_map:
            key, reverse = key_map[choice]
            sorted_students = sorted(self.students, key=lambda x: x[key], reverse=reverse)
        else:
            sorted_students = self.students

        print("\n--- Student List ---")
        for s in sorted_students:
            print(f"ID: {s['id']} | Name: {s['first_name']} {s['last_name']} | Grade: {s['grade']} | Address: {s.get('address', '-')}")
    
    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()
        original_count = len(self.students)
        self.students = [s for s in self.students if s['id'] != student_id]

        if len(self.students) < original_count:
            print("Student deleted.")
        else:
            print("Student not found.")

    def analyze_grades(self):
        if not self.students:
            print("No students to analyze.")
            return

        grades = [s['grade'] for s in self.students]
        average = sum(grades) / len(grades)
        max_grade = max(grades)
        min_grade = min(grades)

        print(f"\nAverage grade: {average:.2f}")
        print(f"Highest grade: {max_grade}")
        print(f"Lowest grade: {min_grade}")

        query = input("Enter student name or ID to search (leave empty to skip): ").strip()
        if query:
            for s in self.students:
                if query == s['id'] or query.lower() in (s['first_name'].lower(), s['last_name'].lower()):
                    print(f"Found: {s['first_name']} {s['last_name']} | Grade: {s['grade']}")
                    break
            else:
                print("Student not found.")
