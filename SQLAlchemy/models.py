from sqlalchemy import create_engine, Column, String, Integer, Table, ForeignKey, Text
from sqlalchemy.orm import declarative_base, Relationship, relationship

CONNECTION_STRING = 'postgresql+psycopg2://postgres:password@localhost/alchemy'

engine = create_engine(CONNECTION_STRING)
Base = declarative_base()

students_subjects_association = Table(
    'students_subjects',
    Base.metadata,
    Column('student_id', ForeignKey('students.id')),
    Column('subject_id', ForeignKey('subjects.id'))
)


class Student(Base):

    __tablename__ = 'students'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer())
    gender = Column(String(10))
    scholarship = Column(Integer())
    subjects = Relationship(
        'Subject',
        secondary=students_subjects_association,
        back_populates='students'
    )


class Subject(Base):

    __tablename__ = 'subjects'
    id= Column(Integer, primary_key=True)
    name = Column(String(20))
    students = Relationship(
        Student,
        secondary=students_subjects_association,
        back_populates='subjects'
    )

class Recipe(Base):

    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)   # models.CharField(max_length=30, null=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)

    chef_id = Column(Integer, ForeignKey('chefs.id'))
    chef = relationship(
        'Chef',
        back_populates='recipes'
    )

class Chef(Base):

    __tablename__ = 'chefs'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    recipes = relationship(
        Recipe,
        back_populates='chef'
    )
