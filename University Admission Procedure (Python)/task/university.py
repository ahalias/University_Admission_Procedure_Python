from data import Applicants, Session, Base, engine


session = Session()


class Admission:

    def __init__(self):
        self.departments = 'Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics'
        self.possible_departments = Applicants.first_department, Applicants.second_department, Applicants.third_department
        self.student_number = 0

    def get_student_number(self):
        self.student_number = int(input())

    def get_student_list(self):
        with open("applicants.txt", "r") as file:
            for string in file:
                line = string.strip().split(" ")
                applicant = Applicants(
                    name=line[0] + ' ' + line[1],
                    physics_grade=line[2],
                    chemistry_grade=line[3],
                    math_grade=line[4],
                    compscience_grade=line[5],
                    special_exam=line[6],
                    first_department=line[7],
                    second_department=line[8],
                    third_department=line[9],
                )
                session.add(applicant)
                session.commit()

    def get_grades(self, students_applied, department):
        for student_entry in students_applied:
            if student_entry.faculty is None:
                if department == "Physics":
                    student_entry.grade = max(student_entry.special_exam,
                                              (student_entry.physics_grade + student_entry.math_grade) / 2)
                elif department == "Chemistry":
                    student_entry.grade = max(student_entry.special_exam, student_entry.chemistry_grade)
                elif department == "Mathematics":
                    student_entry.grade = max(student_entry.special_exam, student_entry.math_grade)
                elif department == "Engineering":
                    student_entry.grade = max(student_entry.special_exam,
                                              (student_entry.compscience_grade + student_entry.math_grade) / 2)
                elif department == "Biotech":
                    student_entry.grade = max(student_entry.special_exam,
                                              (student_entry.physics_grade + student_entry.chemistry_grade) / 2)
                session.commit()

    def admit_students(self):
        for possible_department in self.possible_departments:
            for department in self.departments:
                students_applied = session.query(Applicants).filter(possible_department == department).all()
                self.get_grades(students_applied, department)
                students_applied_rated = session.query(Applicants).filter(possible_department == department).order_by(Applicants.grade.desc(), Applicants.name.asc()).all()
                for student in students_applied_rated:
                    if self.get_faculty_studs(department) != self.student_number and student.faculty is None:
                        student.faculty = department
                        session.commit()
                continue

    def get_faculty_studs(self, dep):
        return session.query(Applicants).filter(Applicants.faculty == dep).count()

    def print_student_list(self):
        for department in self.departments:
            graduated_to_department = session.query(Applicants).filter(Applicants.faculty == department)\
                .order_by(Applicants.grade.desc(), Applicants.name.asc()).all()
            with open(f'{department}.txt', 'w') as file:
                for stud in graduated_to_department:
                    print(f'{stud.name} {stud.grade}', sep='\n', file=file)

    def clean_cache(self):
        Base.metadata.drop_all(engine)


session.close()
