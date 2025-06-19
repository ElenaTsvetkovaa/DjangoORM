import os
import django
from datetime import date

from django.db.models import F, Value
from django.db.models.functions import Replace

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():

    Student.objects.bulk_create(
        (
            Student(
            student_id="FC5204",
            first_name="John",
            last_name="Doe",
            birth_date="1995-05-15",
            email="john.doe@university.com",
            ),
            Student(
                student_id="FE0054",
                first_name="Jane",
                last_name="Smith",
                birth_date=None,
                email="jane.smith@university.com",
            ),
            Student(
                student_id="FH2014",
                first_name="Alice",
                last_name="Johnson",
                birth_date="1998-02-10",
                email="alice.johnson@university.com",
            ),
            Student(
                student_id="FH2015",
                first_name="Bob",
                last_name="Wilson",
                birth_date="1996-11-25",
                email="bob.wilson@university.com",
            ),
        )
    )

def get_students_info():

    students = []

    for s in Student.objects.values_list("student_id", "first_name", "last_name", "email"):
        students.append(f"Student №{s[0]}: {s[1]} {s[2]}; Email: {s[3]}")

    return '\n'.join(students)

def update_students_emails():

    return  Student.objects.filter(email__endswith="university.com").update(
            email=Replace(F("email"), Value("university.com"), Value("uni-students.com")
            ))

def truncate_students():

    Student.objects.all().delete()


