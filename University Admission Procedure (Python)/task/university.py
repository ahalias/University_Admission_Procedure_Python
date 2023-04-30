from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


engine = create_engine('sqlite:///students.db')
Base = declarative_base()


class Applicants(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=False)
    physics_grade = Column(Float, nullable=False)
    chemistry_grade = Column(Float, nullable=False)
    math_grade = Column(Float, nullable=False)
    compscience_grade = Column(Float, nullable=False)
    special_exam = Column(Float, nullable=False)
    first_department = Column(String, nullable=False)
    second_department = Column(String, nullable=False)
    third_department = Column(String, nullable=False)
    grade = Column(Float, nullable=True)
    faculty = Column(String, nullable=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Admission:

    def __init__(self):
        self.departments = 'Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics'
        self.studs_in_faculty = {department: 0 for department in self.departments}
        self.student_number = 0
        self.graduated_studs_list = []


    def get_student_number(self):
        self.student_number = int(input())

    def get_student_list(self):
        with open("applicants.txt", "r") as file:
            for string in file:
                line = string.strip().split(" ")
                applicant = Applicants(
                    name=line[0] + ' ' + line[1],
                    physics_grade=line[2],
                    chemistry_grade = line[3],
                    math_grade = line[4],
                    compscience_grade = line[5],
                    special_exam = line[6],
                    first_department=line[7],
                    second_department=line[8],
                    third_department=line[9],
                )
                session.add(applicant)
                session.commit()

    def admit_students(self, department_number):
        for department in self.departments:
            students_applied = session.query(Applicants).filter(department_number == department).all()
            for student_entry in students_applied:
                if student_entry.name not in self.graduated_studs_list:
                    if department == "Physics":
                        student_entry.grade = max(student_entry.special_exam, (student_entry.physics_grade + student_entry.math_grade)/2)
                    elif department == "Chemistry":
                        student_entry.grade = max(student_entry.special_exam, student_entry.chemistry_grade)
                    elif department == "Mathematics":
                        student_entry.grade = max(student_entry.special_exam, student_entry.math_grade)
                    elif department == "Engineering":
                        student_entry.grade = max(student_entry.special_exam, (student_entry.compscience_grade + student_entry.math_grade)/2)
                    elif department == "Biotech":
                        student_entry.grade = max(student_entry.special_exam, (student_entry.physics_grade + student_entry.chemistry_grade) / 2)
                    session.commit()
            students_applied_rated = session.query(Applicants).filter(department_number == department).order_by(Applicants.grade.desc(), Applicants.name.asc()).all()
            for student in students_applied_rated:
                if self.studs_in_faculty[department] != self.student_number and student.name not in self.graduated_studs_list and student.faculty is None:
                    student.faculty = department
                    self.studs_in_faculty[department] += 1
                    self.graduated_studs_list.append(student.name)
                    session.commit()
            continue

    def print_student_list(self):
        for department in self.departments:
            graduated_to_department = session.query(Applicants).filter(Applicants.faculty == department)\
                .order_by(Applicants.grade.desc(), Applicants.name.asc()).all()

            with open(f'{department}.txt', 'w') as file:
                for stud in graduated_to_department:
                    print(f'{stud.name} {stud.grade}', sep='\n', file=file)

    def clean_cache(self):
        Base.metadata.drop_all(engine)


admission = Admission()
admission.get_student_list()
admission.get_student_number()
admission.admit_students(Applicants.first_department)
admission.admit_students(Applicants.second_department)
admission.admit_students(Applicants.third_department)
admission.print_student_list()
admission.clean_cache()


session.close()
