from operator import itemgetter, attrgetter


class Student:
  def __init__(self, name, gpa, age):
    self.name = name
    self.gpa = gpa
    self.age = age
    return

  def __str__(self):
    return 'Student {} is {} years-old and has {} GPA'.format(self.name, self.age, self.gpa)

  def __lt__(self, other):
    if not type(other) is Student or other is None:
      raise Exception('Cannot compare with non student class')

    if self.gpa > other.gpa:
      return False
    elif self.gpa < other.gpa:
      return True
    else:
      if self.name > other.name:
        return False
      elif self.name < other.name:
        return True
      else:
        if self.age > other.age:
          return False
        elif self.age < other.age:
          return True
        else:
          return False

  def __eq__(self, other):
    if not type(other) is Student or other is None:
      raise Exception('Cannot compare with non student class')

    return self.age == other.age and self.gpa == other.gpa and self.name == other.name

  def __hash__(self):
    return hash(self.gpa) + hash(self.name) + hash(self.age)

  def __repr__(self):
    return repr((self.gpa, self.name, self.age))


if __name__ == '__main__':
  student6 = Student('test6', 1.6, 20)
  student2 = Student('test1', 2, 20)
  student3 = Student('test1', 2, 21)
  student4 = Student('test3', 2, 20)
  student5 = Student('test5', 3, 20)
  student1 = Student('test1', 4, 13)
  student7 = Student('test1', 2, 20)

  students = [student1, student2, student3, student4, student5, student6]

  print('------------------------------------------')
  print('Using sort without lambda')
  print('------------------------------------------')

  sortedStudents = sorted(students)
  for student in sortedStudents:
    print(student)

  print('------------------------------------------')
  print('Using dict')
  print('------------------------------------------')

  studentDict = {}
  for student in students:
    studentDict[student] = student.name

  for k, v in studentDict.items():
    print('{} in dic has value: {}'.format(k, v))

  print('student 7 also in dict: {}'.format(studentDict[student7]))

  sortedStudents_lambda = sorted(students, key=attrgetter('gpa', 'name', 'age'))
  print('------------------------------------------')
  print('Using lambda')
  print('------------------------------------------')
  for student in sortedStudents_lambda:
    print(student)
