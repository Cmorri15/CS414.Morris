#include <iostream>
#include <string>

class Person {
public:
    std::string name;

    Person(const std::string& person_name) : name(person_name) {
        std::cout << "Initializing Person: " << name << '\n';
    }
};

class Student : public Person {
public:
    std::string major;

    Student(const std::string& person_name, const std::string& student_major)
        : Person(person_name), major(student_major) {
        std::cout << "Initializing Student\n";
    }
};

class Employee : public Person {
public:
    int employee_id;

    Employee(const std::string& person_name, int id)
        : Person(person_name), employee_id(id) {
        std::cout << "Initializing Employee\n";
    }
};

class TeachingAssistant : public Student, public Employee {
public:
    std::string course;

    TeachingAssistant(const std::string& person_name,
                      const std::string& student_major,
                      int id,
                      const std::string& assigned_course)
        : Student(person_name, student_major),
          Employee(person_name, id),
          course(assigned_course) {
        std::cout << "Initializing TeachingAssistant\n";
    }
};

int main() {
    TeachingAssistant ta(
        "Alex Rivera",
        "Computer Science",
        1042,
        "CS 240"
    );

    std::cout << "\n--- Person subobjects ---\n";

    Person& student_person = static_cast<Student&>(ta);
    Person& employee_person = static_cast<Employee&>(ta);

    std::cout << "Student Person address: "
              << static_cast<const void*>(&student_person) << '\n';
    std::cout << "Student Person name: "
              << student_person.name << '\n';

    std::cout << "Employee Person address: "
              << static_cast<const void*>(&employee_person) << '\n';
    std::cout << "Employee Person name: "
              << employee_person.name << '\n';

    std::cout << "\n--- Change one name ---\n";

    student_person.name = "Alex Student";

    std::cout << "Student Person name: "
              << student_person.name << '\n';
    std::cout << "Employee Person name: "
              << employee_person.name << '\n';

    // std::cout << ta.name << '\n';

    // Person* person = &ta;

    return 0;
}