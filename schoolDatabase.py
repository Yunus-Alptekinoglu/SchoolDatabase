

import random


class Course:


    def __init__(self, cid, cname, credits):
        self.cid = cid
        self.cname = cname
        self.credits = credits


    def __str__(self):
        return f'{self.cid}({self.credits}): {self.cname}'


    __repr__ = __str__


    # Checks if self and other are equal by checking if other is of type Course and if self and other have the same id
    def __eq__(self, other):
        if isinstance(other, Course) and self.cid == other.cid:
            return True
        else:
            return False


class Catalog:


    def __init__(self):
        self.courseOfferings = {}


    # Adds a course to courseOfferings where the id is the key and the course is the value
    def addCourse(self, cid, cname, credits):
        if cid in self.courseOfferings:
            return 'Course already added'
        else:
            self.courseOfferings[cid] = Course(cid, cname, credits)
            return 'Course added successfully'
        

    # Removes a course from courseOfferings by deleting the key value pair associated with the given id
    def removeCourse(self, cid):
        if cid not in self.courseOfferings:
            return 'Course not found'
        else:
            del self.courseOfferings[cid]
            return 'Course removed successfully'
        

    # Reads the catalog file, splits it into a list of course id; course name; and course credits, and adds it to courseOfferings
    def _loadCatalog(self, file):
        with open(file, "r") as f:
            course_info = f.read()
            updated_course_info = course_info.split('\n')
            for course in updated_course_info:
                final_course_info = course.split(',')
                self.addCourse(final_course_info[0], final_course_info[1], int(final_course_info[2]))
        

class Semester:


    def __init__(self):
        self.courses = {}


    def __str__(self):
        if self.courses == {}:
            return 'No courses'
        else:
            return '; '.join(self.courses.keys())


    __repr__ = __str__


    # Adds a course to the courses dictionary, where the id of the course is the key and the course is the value
    def addCourse(self, course):
        if course in self.courses.values():
            return 'Course already added'
        else:
            self.courses[course.cid] = course


    # Drops a course by deleting the key value pair associated with the id of the given course
    def dropCourse(self, course):
        if course not in self.courses.values():
            return 'No such course'
        else:
            del self.courses[course.cid]


    # Returns the total credits a student is taking by iterating through each course in the courses dictionary and adding the credit count of each course to a counter variable
    @property
    def totalCredits(self):
        credits_count = 0
        for course in self.courses.values():
            credits_count += course.credits
        return credits_count


    # Checks if a student is full time by checking if the total credits they're taking is greater than 12
    @property
    def isFullTime(self):
        if self.totalCredits >= 12:
            return True
        else:
            return False

    
class Loan:
    

    def __init__(self, amount):
        self.loan_id = self.__getloanID
        self.amount = amount


    def __str__(self):
        return f'Balance: ${self.amount}'


    __repr__ = __str__


    # Returns a loan's id by generating a random number in the given range and setting the id of the loan to that number
    @property
    def __getloanID(self):
        number = random.randint(10000, 99999)
        self.loan_id = number
        return self.loan_id


class Person:


    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn


    def __str__(self):
        return f'Person({self.name}, ***-**-{self.ssn[-4:]})'


    __repr__ = __str__


    def get_ssn(self):
        return self.ssn


    # Checks if self and other are equal by checking if other is of type Person and if self and other have the same ssn
    def __eq__(self, other):
        if isinstance(other, Person) and self.ssn == other.ssn:
            return True
        else:
            return False


    # Returns the initials of a student by splitting each name in their full name into a list, iterating through the list, and combining the first letter in each of their names into a string
    @property
    def initials(self):
        initials = ''
        name_lst = self.name.split(' ')
        for name in name_lst:
            initial = name[0].lower()
            initials += initial
        return initials


class Staff(Person):


    def __init__(self, name, ssn, supervisor=None):
        super().__init__(name, ssn)
        self.__supervisor = supervisor


    def __str__(self):
        return f'Staff({self.name}, {self.id})'


    __repr__ = __str__


    @property
    def id(self):
        return f'905{self.initials}{self.ssn[-4:]}'


    @property   
    def getSupervisor(self):
        return self.__supervisor


    # Sets a supervisor by checking if new_supervisor is of type Staff and assigning it to getSupervisor if it is
    def setSupervisor(self, new_supervisor):
        if isinstance(new_supervisor, Staff):
            new_supervisor = self.getSupervisor
            return 'Completed!'


    # Applies a hold on a student by checking if student is of type Student and setting hold to True if it is
    def applyHold(self, student):
        if isinstance(student, Student):
            student.hold = True
            return 'Completed!'
        

    # Removes a hold from a student by checking if student is of type Student and setting hold to False if it is
    def removeHold(self, student):
        if isinstance(student, Student):
            student.hold = False
            return 'Completed!'
        

    # Unenrolls a student by checking if student is of type Student and setting active to False if it is
    def unenrollStudent(self, student):
        if isinstance(student, Student):
            student.active = False
            return 'Completed'
        

    def createStudent(self, person):
        return Student(person.name, person.get_ssn(), 'Freshman')


class Student(Person):


    def __init__(self, name, ssn, year):
        random.seed(1)
        super().__init__(name, ssn)
        self.year = year
        self.classCode = ''
        self.semesters = {}
        self.hold = False
        self.active = True
        self.account = self.__createStudentAccount()


    def __str__(self):
        return f'Student({self.name}, {self.id}, {self.get_year})'


    __repr__ = __str__


    def __createStudentAccount(self):
        if self.active == True:
            return StudentAccount(self)


    @property
    def id(self):
        return f'{self.initials}{self.ssn[-4:]}'


    # Determines the year of a student by checking the current semester of the student
    @property
    def get_year(self):
        if self.active == False or self.hold == True:
            return 'Unsuccessful operation'
        else:
            new_semester = len(self.semesters)
            if new_semester <= 1 or new_semester == 2:
                self.classCode = 'Freshman'
            elif new_semester == 3 or new_semester == 4:
                self.classCode = 'Sophomore'
            elif new_semester == 5 or new_semester == 6:
                self.classCode = 'Junior'
            else:
                self.classCode = 'Senior'
        return self.classCode


    # Registers a new semester to semesters where the new semester is the key and the semester object is the value
    def registerSemester(self):
        if self.active == False or self.hold == True:
            return 'Unsuccessful operation'
        else:
            new_key = (len(self.semesters) + 1)
            self.semesters[new_key] = Semester()
    
    
    # Enrolls a student in a course by adding the course to the current semester and charging the student the price of the course
    def enrollCourse(self, cid, catalog):
        current_semester = self.semesters[len(self.semesters)]
        if self.active == False or self.hold == True:
            return 'Unsuccessful operation'
        if cid not in catalog.courseOfferings:
            return 'Course not found'
        if cid in current_semester.courses:
            return 'Course already enrolled'
        course_object = catalog.courseOfferings[cid]
        current_semester.addCourse(course_object)
        self.account.chargeAccount(course_object.credits * StudentAccount.CREDIT_PRICE)
        return 'Course added successfully'


    # Drops a course by refunding the student half of the price of the course and deleting the course from the courses dictionary
    def dropCourse(self, cid):
        current_semester = self.semesters[len(self.semesters)]
        if self.active == False or self.hold == True:
            return 'Unsuccessful operation'
        if cid not in current_semester.courses:
            return 'Course not found'
        self.account.makePayment((current_semester.courses[cid].credits * StudentAccount.CREDIT_PRICE) / 2)
        current_semester.dropCourse(current_semester.courses[cid])
        return 'Course dropped successfully'
    

    # Sends a student a loan by making a payment equal to the amount of the loan to the student's account
    def getLoan(self, amount):
        loan_object = Loan(amount)
        self.account.loans[loan_object.loan_id] = loan_object
        self.account.makePayment(amount)


class StudentAccount:


    CREDIT_PRICE = 1000


    def __init__(self, student):
        self.student = student
        self.balance = 0
        self.loans = {}


    def __str__(self):
        return f'Name: {self.student.name}\nID: {self.student.id}\nBalance: ${self.balance}'


    __repr__ = __str__


    # A payment is made by subtracting the payment amount from the student's balance
    def makePayment(self, amount):
        self.balance -= amount
        return self.balance


    # A payment is received by adding the payment amount to the student's balance
    def chargeAccount(self, amount):
        self.balance += amount
        return self.balance

