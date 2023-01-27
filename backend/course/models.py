import os

from django.db import models
from django.contrib.auth.models import User


class Semester(models.Model):
    SEMESTERS = (
        (1, "Fall"),
        (2, "Spring"),
        (3, "Summer"),
    )

    year = models.IntegerField()
    semester = models.IntegerField(choices=SEMESTERS)
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    description = models.TextField()
    syllabus = models.FileField(upload_to="syllabus", blank=True)

    class Meta:
        unique_together = ("year", "semester")
        ordering = ["-year", "semester"]

    def __str__(self):
        return self.get_semester_display() + " " + str(self.year)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.IntegerField()
    academic_email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="TAs/images", blank=True)

    def __str__(self):
        return (
            self.user.first_name + " " + self.user.last_name
            if self.user.first_name and self.user.last_name
            else self.user.username
        )


class Instruction(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = ("person", "semester")

    def __str__(self):
        return f"{str(self.person)} @ {str(self.semester)}"


class TeachingAssisting(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = ("person", "semester")

    def __str__(self):
        return f"{str(self.person)} @ {str(self.semester)}"


class Enrolling(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = ("person", "semester")

    def __str__(self):
        return f"{str(self.person)} @ {str(self.semester)}"


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class FileMaterial(Material):
    ACCESS_CONTROL_CHOICES = (
        (0, "Public"),
        (1, "Student"),
        (2, "TA"),
        (3, "Admin"),
    )

    file = models.FileField(upload_to="files/")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    access_control = models.IntegerField(choices=ACCESS_CONTROL_CHOICES)

    def get_person_access(self, person):
        if person is None:
            return 0
        if person.user.is_superuser:
            return 3
        if TeachingAssisting.objects.filter(
            person=person,
            semester=self.semester,
        ).exists():
            return 2
        if Enrolling.objects.filter(
            person=person,
            semester=self.semester,
        ).exists():
            return 1
        return 0

    def get_user_access(self, user):
        if user is None:
            return 0
        return self.get_person_access(user.person)

    def has_access(self, user):
        return self.get_user_access(user) >= self.access_control

    def get_file_name(self):
        original_file_name, file_extension = os.path.splitext(self.file.name)
        return self.name + file_extension

    def get_url(self):
        return f"/api/course/file/{self.get_file_name()}"

    def __str__(self):
        return f"File {self.name} @ {str(self.semester)}"


class URLMaterial(Material):
    url = models.URLField()

    def get_url(self):
        return self.url

    def __str__(self):
        return f"URL {self.name} @ {str(self.semester)}"


class Session(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    description = models.TextField()
    files = models.ManyToManyField(
        FileMaterial, blank=True, related_name="session_files"
    )
    urls = models.ManyToManyField(URLMaterial, blank=True, related_name="session_urls")

    def __str__(self):
        return f"Session {self.title} @ {str(self.semester)}"


class Assignment(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    description = models.TextField()
    questions = models.ForeignKey(
        FileMaterial, on_delete=models.RESTRICT, related_name="questions"
    )
    solutions = models.ForeignKey(
        FileMaterial, on_delete=models.RESTRICT, related_name="solutions"
    )
    files = models.ManyToManyField(
        FileMaterial, blank=True, related_name="assignment_files"
    )
    urls = models.ManyToManyField(
        URLMaterial, blank=True, related_name="assignment_urls"
    )

    def __str__(self):
        return f"Assignment {self.title} @ {str(self.semester)}"


class Submission(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    delay = models.IntegerField()

    class Meta:
        unique_together = ("person", "assignment")

    def __str__(self):
        return f"Submission {str(self.person)} for {str(self.assignment)}"


class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question_identifier = models.CharField(max_length=100)


class Grade(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    grade = models.IntegerField()

    class Meta:
        unique_together = ("person", "question")

    def __str__(self):
        return f"Grade {str(self.question)} for {str(self.person.employee_id)}"


class Objection(models.Model):
    STATE_CHOICES = (
        (0, "Created"),
        (1, "Accepted"),
        (2, "Rejected"),
    )

    state = models.IntegerField(choices=STATE_CHOICES, default=0)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    current_grade = models.IntegerField()
    objection_text = models.TextField()
    response_text = models.TextField(blank=True)

    class Meta:
        unique_together = ("person", "question")

    def __str__(self):
        return f"Objection @ {str(self.grade)}"
