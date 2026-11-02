class Person:
    def __init__(self, *, name, **kwargs):
        print(f"Entering Person.__init__(), id(self)={id(self)}")
        self.name = name
        super().__init__(**kwargs)

    def role(self):
        return "Person"


class Student(Person):
    def __init__(self, *, major, **kwargs):
        print(f"Entering Student.__init__(), id(self)={id(self)}")
        self.major = major
        super().__init__(**kwargs)
        
    def change_name_from_student(self):
        self.name = "Name changed by Student"

    def role(self):
        return "Student"


class Employee(Person):
    def __init__(self, *, employee_id, **kwargs):
        print(f"Entering Employee.__init__(), id(self)={id(self)}")
        self.employee_id = employee_id
        super().__init__(**kwargs)

    def change_name_from_employee(self):
        self.name = "Name changed by Employee"

    def role(self):
        return "Employee"

class TeachingAssistant(Student, Employee):
    def __init__(self, *, course, **kwargs):
        print(
            f"Entering TeachingAssistant.__init__(), "
            f"id(self)={id(self)}"
        )
        self.course = course
        super().__init__(**kwargs)

    def role(self):
        return "Teaching Assistant"

class ReversedTeachingAssistant(Employee, Student):
    def __init__(self, *, course, **kwargs):
        self.course = course
        super().__init__(**kwargs)

class RobotAssistant:
    def role(self):
        return "Robot Assistant"

ta = TeachingAssistant(
    name="Alex Rivera",
    major="Computer Science",
    employee_id=1042,
    course="CS 240",
)

print("\n--- Method Resolution Order ---")
print(TeachingAssistant.__mro__)

print("\n--- Object State ---")
print(vars(ta))

print("\n--- Change name through Student ---")
ta.change_name_from_student()
print("Name:", ta.name)

print("\n--- Change name through Employee ---")
ta.change_name_from_employee()
print("Name:", ta.name)
print("Object State:", vars(ta))

print("\n--- Method Resolution Test ---")
print("Role:", ta.role())

print("\n--- Reversed Teaching Assistant ---")

reversed_ta = ReversedTeachingAssistant(
    name="Alex Rivera",
    major="Computer Science",
    employee_id=1042,
    course="CS 240",
)

print("MRO:", ReversedTeachingAssistant.__mro__)
print("Role:", reversed_ta.role())

def announce(value):
    print(value.role())

print("\n--- Unrelated Class Test ---")

robot = RobotAssistant()

announce(ta)
announce(robot)

try:
    announce(42)
except AttributeError as error:
    print("Error:", error)