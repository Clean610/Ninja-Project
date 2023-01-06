import uuid

from apis.models import Schools, Headmaster, Class, Student, Teacher
from ninja import ModelSchema, Schema, Field


class SchoolSchema(ModelSchema):
    class Config:
        model = Schools
        model_fields = ['id', 'title']


class HeadMasterSchemaIn(Schema):
    school: int = None
    first_name: str = None
    last_name: str = None


class HeadMasterSchemaOut(ModelSchema):
    school: SchoolSchema = None

    class Config:
        model = Headmaster
        model_fields = ['id', 'first_name', 'last_name']


class ClassSchemaOut(Schema):
    school: int = None
    title: str = None
    number_of_student: int = None


class ClassSchemaIn(ModelSchema):
    school: SchoolSchema = None

    class Config:
        model = Class
        model_fields = ['id', 'title', 'number_of_student']


class StudentSchemaOut(ModelSchema):
    classroom: ClassSchemaIn = None

    class Config:
        model = Student
        model_fields = ['id', 'first_name', 'last_name', 'student_id']


class StudentSchemaIn(Schema):
    first_name: str = None
    last_name: str = None
    classroom: int = None
    student_id: uuid.UUID = uuid.uuid4()


class TeacherSchemaOut(ModelSchema):
    classroom: ClassSchemaIn = None

    class Config:
        model = Student
        model_fields = ['id', 'first_name', 'last_name']


class TeacherSchemaIn(Schema):
    first_name: str = None
    last_name: str = None
    classroom: int = None
