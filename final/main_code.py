from file_handler import load_students, save_students
import student_manager

FILENAME = "students.json"

def main():
    students = load_students(FILENAME)

    while True:
        print("\n--- Student Grade Management System ---")
        print("1. Add student")
        print("2. View students")
        print("3. Delete student")
        print("4. Grade statistics")
        print("5. Save and Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            student_manager.add_student(students)
        elif choice == "2":
            student_manager.display_students(students)
        elif choice == "3":
            student_manager.delete_student(students)
        elif choice == "4":
            student_manager.analyze_grades(students)
        elif choice == "5":
            save_students(students, FILENAME)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
