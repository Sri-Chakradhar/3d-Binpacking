class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    def get_grade(self):
        return self.grade
class Course:
    def __init__(self, name, max_number):
        self.name = name
        self.max_number = max_number
        self.students=[]
    def add_student(self, student):
        if len(self.students) < self.max_number:
            self.students.append(student)
            return True
        return False
    def get_average(self):
        value = 0
        for student in self.students:
            value += student.get_grade()
        
        return value / len(self.students)

s1=Student('Tim', 19, 71)
s2=Student("bim", 19, 72)
s3=Student("bat", 79, 78)

course=Course("Science",2)
course.add_student(s1)
course.add_student(s2)
print(course.add_student(s3))
print(course.get_average())
        
