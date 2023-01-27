from django.contrib import admin

from .models import (
    Semester,
    Person,
    Instruction,
    TeachingAssisting,
    Enrolling,
    Material,
    FileMaterial,
    URLMaterial,
    Session,
    Assignment,
    Submission,
    Question,
    Grade,
    Objection
)


admin.site.register(Semester)
admin.site.register(Person)
admin.site.register(Instruction)
admin.site.register(TeachingAssisting)
admin.site.register(Enrolling)
admin.register(Material)
admin.site.register(FileMaterial)
admin.site.register(URLMaterial)
admin.site.register(Session)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Question)
admin.site.register(Grade)
admin.site.register(Objection)
