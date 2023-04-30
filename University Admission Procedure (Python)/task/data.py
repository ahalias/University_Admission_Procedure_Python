from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base


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
