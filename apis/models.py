# ---------- Python's Libraries ---------------------------------------------------------------------------------------
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
# ---------- Django Tools  --------------------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

from safedelete.models import SafeDeleteModel, SOFT_DELETE
# ---------- Created Tools --------------------------------------------------------------------------------------------


# ========= Base Model ================================================================================================
class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    original_objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Schools(BaseModel):
    title = models.CharField(max_length=20, blank=False, null=False)

    @property
    def details_context(self):
        return {
            "id": self.pk,
            "title": self.title,
        }

    class Meta:
        constraints = [models.UniqueConstraint(fields=["title"],
                                               condition=Q(deleted__isnull=True), name="unique_school_title")]


class Headmaster(BaseModel):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    school = models.ForeignKey(Schools, blank=False, null=False, on_delete=models.CASCADE)

    @property
    def details_context(self):
        return {
            "id": self.pk,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "school": self.school.details_context,
        }


class Class(BaseModel):
    title = models.CharField(max_length=20, blank=False, null=False)
    number_of_student = models.IntegerField(blank=False, null=False,
                                            validators=[MinValueValidator(0), MaxValueValidator(50)])
    school = models.ForeignKey(Schools, blank=False, null=False, on_delete=models.CASCADE)

    @property
    def details_context(self):
        return {
            "id": self.pk,
            "title": self.title,
            "number_of_student": self.number_of_student,
        }

    class Meta:
        constraints = [models.UniqueConstraint(fields=["title"],
                                               condition=Q(deleted__isnull=True), name="unique_class_title")]


class Student(BaseModel):
    classroom = models.ForeignKey(Class, blank=False, null=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    student_id = models.UUIDField(null=False, blank=False, default=uuid.uuid4, editable=True)

    @property
    def details_context(self):
        return {
            "id": self.pk,
            "classroom": self.classroom.details_context,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "student_id": self.student_id
        }


class Teacher(BaseModel):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    classroom = models.ForeignKey(Class, blank=True, null=True, on_delete=models.CASCADE)

    @property
    def details_context(self):
        return {
            "id": self.pk,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
