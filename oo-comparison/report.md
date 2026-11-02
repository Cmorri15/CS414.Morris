# Object-Oriented Inheritance Comparison

## 1. Nonvirtual and Virtual Inheritance in C++

In the nonvirtual diamond, `TeachingAssistant` inherits from both `Student` and `Employee`, and both inherit from `Person`. Without virtual inheritance, the teaching assistant contains two separate `Person` subobjects. The program showed that the two subobjects had different memory addresses and could store different names. Accessing `ta.name` directly was ambiguous because the compiler could not determine which `Person` subobject to use.

In the virtual diamond, `Student` and `Employee` inherit virtually from `Person`. The `TeachingAssistant` then contains only one shared `Person` subobject. The program showed that both paths had the same memory address and that changing the name through one path changed the name seen through the other. The most-derived class, `TeachingAssistant`, initializes the shared virtual `Person` base.

## 2. Virtual Functions in C++

The `Person` class defines a virtual `role()` function. `Student`, `Employee`, and `TeachingAssistant` override it. Calling `role()` through a `Person` reference to a `TeachingAssistant` produced `Teaching Assistant`. This demonstrates runtime polymorphism: the function implementation is selected according to the object's actual type.

When `Student` and `Employee` each override `role()`, the `TeachingAssistant` class must provide its own override to resolve the competing final overriders. Otherwise, the class is ill-formed and the compiler reports an error.

## 3. Cooperative Multiple Inheritance in Python

The Python implementation uses `super()` and keyword arguments to pass initialization through the inheritance hierarchy. The initializer output showed the same object identity at each step, demonstrating that the methods initialize one shared object rather than separate `Person` objects.

The method resolution order (MRO) for `TeachingAssistant(Student, Employee)` was `TeachingAssistant`, `Student`, `Employee`, `Person`, and `object`. Since `Student` appears before `Employee`, Python selects `Student.role()` when the child class does not define its own `role()` method. When `TeachingAssistant` defines its own method, that method is selected instead.

Reversing the parent order to `ReversedTeachingAssistant(Employee, Student)` reversed the order of `Employee` and `Student` in the MRO. Without a `role()` override in the reversed class, Python selected `Employee.role()`.

## 4. Unrelated Types and Polymorphism

Python's `announce()` function worked with both `TeachingAssistant` and the unrelated `RobotAssistant` because both classes provided a `role()` method. Passing an integer caused an `AttributeError` because integers do not provide that method. This demonstrates duck typing: Python attempts to use the operations an object supports rather than requiring a particular inheritance relationship.

In C++, the `announce_generic()` function template worked with both `TeachingAssistant` and `RobotAssistant` because both provided a compatible `role()` method. However, `announce_person()` accepts a `const Person&`, so it worked with `TeachingAssistant` but failed to compile when passed a `RobotAssistant`. This demonstrates the difference between template-based generic programming and a function requiring a specific base-class interface.

## 5. Conclusion

These experiments demonstrate that inheritance and polymorphism work differently across C++ and Python. C++ virtual inheritance controls whether a diamond hierarchy shares a base-class subobject, while virtual functions support runtime polymorphism. Python's cooperative initialization and MRO determine how initialization and method lookup proceed through multiple inheritance. Both languages can support unrelated types through generic mechanisms, but their requirements and error handling differ.