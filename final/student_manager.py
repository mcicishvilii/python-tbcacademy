from utils import generate_id

def add_student(students):
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    address = input("Enter address (optional): ").strip()
    
    try:
        grade = float(input("Enter grade (0-100): ").strip())
    except ValueError:
        print("Invalid grade. Must be a number.")
        return

    student = {
        "id": generate_id(),
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "grade": grade
    }

    students.append(student)
    print("Student added successfully.")

def display_students(students):
    if not students:
        print("No students to display.")
        return

    print("\nSort by:")
    print("1. First name (asc)")
    print("2. First name (desc)")
    print("3. Last name (asc)")
    print("4. Last name (desc)")
    print("5. Grade (asc)")
    print("6. Grade (desc)")
    choice = input("Choose option: ").strip()

    key_map = {
        "1": ("first_name", False),
        "2": ("first_name", True),
        "3": ("last_name", False),
        "4": ("last_name", True),
        "5": ("grade", False),
        "6": ("grade", True),
    }

    key, reverse = key_map.get(choice, ("id", False))
    sorted_students = sorted(students, key=lambda s: s[key], reverse=reverse)

    print("\n--- Student List ---")
    for s in sorted_students:
        print(f"ID: {s['id']} | Name: {s['first_name']} {s['last_name']} | Grade: {s['grade']} | Address: {s.get('address', '-')}")

def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()
    found = False

    for i in range(len(students)):
        if students[i]["id"] == student_id:
            found = True
            del students[i]
            print("Student deleted.")
            break

    if not found:
        print("Student not found.")

def analyze_grades(students):
    if not students:
        print("No students to analyze.")
        return

    grades = [s["grade"] for s in students]
    average = sum(grades) / len(grades)
    highest = max(grades)
    lowest = min(grades)

    print("\nGrades:")
    print(f"Average: {average:.2f}")
    print(f"Highest: {highest}")
    print(f"Lowest: {lowest}")

    search = input("Search by student name or ID (leave blank to skip): ").strip().lower()
    if search:
        for s in students:
            if search == s["id"] or search in s["first_name"].lower() or search in s["last_name"].lower():
                print(f"Found: {s['first_name']} {s['last_name']} | Grade: {s['grade']}")
                return
        print("Student not found.")
