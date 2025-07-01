from student_manager import StudentManager
from file_handler import load_students, save_students

def main():
    students = load_students("students.json")
    manager = StudentManager(students)

    while True:
        print("\n--- Student Grade Management System ---")
        print("1. Add student")
        print("2. View students")
        print("3. Delete student")
        print("4. Grade statistics")
        print("5. Save and Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.display_students()
        elif choice == "3":
            manager.delete_student()
        elif choice == "4":
            manager.analyze_grades()
        elif choice == "5":
            save_students(manager.students, "students.json")
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
