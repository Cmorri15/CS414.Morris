#include <iostream>
#include <string>

class Person {
public:
    std::string name;

    Person(const std::string& person_name) : name(person_name) {
        std::cout << "Initializing Person: " << name << '\n';
    }

    virtual std::string role() const {
        return "Person";
    }

    virtual ~Person() = default;
};

class Student : virtual public Person {
public:
    std::string major;

    Student(const std::string& person_name, const std::string& student_major)
        : Person(person_name), major(student_major) {
        std::cout << "Initializing Student\n";
    }

    std::string role() const override {
        return "Student";
    }
};

class Employee : virtual public Person {
public:
    int employee_id;

    Employee(const std::string& person_name, int id)
        : Person(person_name), employee_id(id) {
        std::cout << "Initializing Employee\n";
    }

    std::string role() const override {
        return "Employee";
    }
};

class TeachingAssistant : public Student, public Employee {
public:
    std::string course;

    TeachingAssistant(const std::string& person_name,
                      const std::string& student_major,
                      int id,
                      const std::string& assigned_course)
        : Person(person_name),
          Student(person_name, student_major),
          Employee(person_name, id),
          course(assigned_course) {
        std::cout << "Initializing TeachingAssistant\n";
    }

    std::string role() const override {
        return "Teaching Assistant";
    }
};

class RobotAssistant {
public:
    std::string role() const {
        return "Robot Assistant";
    }
};

void announce_person(const Person& person) {
    std::cout << person.role() << '\n';
}

template<typename T>
void announce_generic(const T& value) {
    std::cout << value.role() << '\n';
}

int main() {
    TeachingAssistant ta(
        "Alex Rivera",
        "Computer Science",
        1042,
        "CS 240"
    );

    std::cout << "\n--- Person subobject ---\n";

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

    std::cout << "\n--- Direct access ---\n";

    std::cout << "Teaching assistant name: "
              << ta.name << '\n';

    Person* person = &ta;

    std::cout << "Person pointer name: "
              << person->name << '\n';

    std::cout << "\n--- Virtual function ---\n";

    Person& person_ref = ta;
    std::cout << "Role: " << person_ref.role() << '\n';

    std::cout << "\n--- Generic Function Test ---\n";

    RobotAssistant robot;

    announce_generic(ta);
    announce_generic(robot);

    std::cout << "\n--- Base-Class Function Test ---\n";

    announce_person(ta);

    // announce_person(robot);

    return 0;
}