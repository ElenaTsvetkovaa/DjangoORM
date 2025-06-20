import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Lecturer, Subject, Student, StudentEnrollment



subject = Subject.objects.get(id=2)
students_enrollments = subject.studentenrollment_set.all().filter(
    student__last_name__icontains='o')

for se in students_enrollments:
    print(subject)
    print(str(se.student))