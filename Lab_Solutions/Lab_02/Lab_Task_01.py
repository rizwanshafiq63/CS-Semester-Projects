# AIC262 – Lab 02 – Graded Lab Task 1
from __future__ import annotations
import sys
import tracemalloc  # For (ix) & (x) memory tests
from dataclasses import dataclass # For (x)

print("\n=== (i) Create instance of a class & display its namespace (instance __dict__) ===")
class MyThing:
    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b

inst = MyThing(a=10, b=20)
print("Instance namespace:", inst.__dict__)  # namespace of the instance


print("\n=== (ii) student_data(student_id, student_name?, student_class?) ===")
def student_data(student_id, student_name=None, student_class=None):
    print(f"ID: {student_id}")
    if student_name is not None:
        print(f"Name: {student_name}")
    if student_class is not None:
        print(f"Class: {student_class}")

# demos
student_data(101)
student_data(102, student_name="Ayesha")
student_data(103, student_class="BS-AI")
student_data(104, "Bilal", "BS-CS")


print("\n=== (iii) Simple Student class: show type, __dict__ keys, and __module__ ===")
class Student:
    pass

print("type(Student):", type(Student))
print("__dict__ keys:", list(Student.__dict__.keys()))
print("__module__:", Student.__module__)


print("\n=== (iv) Two empty classes; check instances and subclass of object ===")
class StudentEmpty:
    pass
class Marks:
    pass

s1 = StudentEmpty()
m1 = Marks()
print("isinstance(s1, StudentEmpty)?", isinstance(s1, StudentEmpty))
print("isinstance(m1, Marks)?", isinstance(m1, Marks))
print("issubclass(StudentEmpty, object)?", issubclass(StudentEmpty, object))
print("issubclass(Marks, object)?", issubclass(Marks, object))


print("\n=== (v) Student with attributes (student_name, marks); modify and show ===")
class StudentMarks:
    def __init__(self, student_name, marks):
        self.student_name = student_name
        self.marks = marks

sm = StudentMarks("Hina", 82)
print("Original:", sm.student_name, sm.marks)
# modify
sm.student_name = "Hina Ali"
sm.marks = 88
print("Modified:", sm.student_name, sm.marks)


print("\n=== (vi) Student with id/name; add student_class; then remove student_name ===")
class StudentIDName:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name

sidn = StudentIDName(201, "Khan")
# add new attribute
sidn.student_class = "BS-SE"
print("With new attribute:", vars(sidn))
# remove name
delattr(sidn, "student_name")
print("After removing student_name:", vars(sidn))


print("\n=== (vii) Student with id/name; add student_class; method to display all attrs ===")
class StudentFull:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.student_class = None  # will be set later

    def display_all(self):
        for k, v in vars(self).items():
            print(f"{k}: {v}")

sf = StudentFull(301, "Maria")
sf.student_class = "BS-DS"
sf.display_all()


print("\n=== (viii) Two instances student1, student2; print attributes in the given format ===")
class StudentPrintable:
    def __init__(self, student_id, student_name, student_class=None):
        self.student_id = student_id
        self.student_name = student_name
        self.student_class = student_class

    def pretty(self):
        return f"[ID={self.student_id}] {self.student_name} (Class: {self.student_class})"

student1 = StudentPrintable(401, "Ahmad", "BS-AI")
student2 = StudentPrintable(402, "Sara", "BS-CS")
print(student1.pretty())
print(student2.pretty())


print("\n=== (ix) Memory allocation tests on the created Python class (tracemalloc) ===")
# Compare a normal class (has per-instance __dict__) vs a slotted class (no per-instance dict)
class StudentNoSlots:
    def __init__(self, student_id, student_name, student_class):
        self.student_id = student_id
        self.student_name = student_name
        self.student_class = student_class

class StudentSlots:
    __slots__ = ("student_id", "student_name", "student_class")  # memory saver
    def __init__(self, student_id, student_name, student_class):
        self.student_id = student_id
        self.student_name = student_name
        self.student_class = student_class

def allocate_many(cls, n=100_000):
    # Create n students to observe memory behaviour
    return [cls(i, f"Name{i}", "BS-AI") for i in range(n)]

def profile_allocation(make_func):
    tracemalloc.start()
    objs = make_func()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"    current={current} bytes, peak={peak} bytes")
    # keep objs alive to prevent GC during measurement
    return objs

print("StudentNoSlots:")
hold1 = profile_allocation(lambda: allocate_many(StudentNoSlots, n=20_000))

print("StudentSlots (__slots__):")
hold2 = profile_allocation(lambda: allocate_many(StudentSlots, n=20_000))


print("\n=== (x) Reduce memory allocation using different techniques ===")
# 1) __slots__ already shown above to remove per-instance dict overhead.
# 2) Use dataclasses with slots for compact, typed instances.
# from dataclasses import dataclass

@dataclass(slots=True)
class StudentDataClass:
    student_id: int
    student_name: str
    student_class: str

print("DataClass with slots (compact instances):")
hold3 = profile_allocation(lambda: allocate_many(StudentDataClass, n=20_000))

# 3) Use tuples for fixed records instead of dicts/lists when mutation isn't needed.
# 4) Intern repeated strings to share a single copy in memory.
def allocate_with_intern(n=50_000):
    label = sys.intern("BS-AI")  # ensure a single shared string object
    return [(i, f"Name{i}", label) for i in range(n)]

print("Tuple records with interned string label (compact, immutable records):")
hold4 = profile_allocation(lambda: allocate_with_intern(50_000))

print("\nAll Lab 02 Task 1 parts (i–x) completed.")

