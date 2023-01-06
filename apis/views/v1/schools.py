# ---------- Python's Libraries ---------------------------------------------------------------------------------------

# ---------- Django Tools  --------------------------------------------------------------------------------------------
from ninja import NinjaAPI
from apis.schemas import SchoolSchema, HeadMasterSchemaOut, HeadMasterSchemaIn, ClassSchemaIn, ClassSchemaOut, \
    StudentSchemaIn, StudentSchemaOut, TeacherSchemaIn, TeacherSchemaOut
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate, LimitOffsetPagination
from safedelete.models import SOFT_DELETE_CASCADE
# ---------- Created Tools --------------------------------------------------------------------------------------------
from apis.models import Schools, Headmaster, Class, Student, Teacher

api = NinjaAPI(version='v1')


class SchoolAPI:

    @staticmethod
    @api.get("/schools", response=list[SchoolSchema])
    @paginate(LimitOffsetPagination)
    def get_list_school(request):

        schools = Schools.objects.all()

        return schools

    @staticmethod
    @api.post("/schools")
    def create_school(request, payload: SchoolSchema):

        school = Schools.objects.create(**payload.dict())

        return {"id": school.id}

    @staticmethod
    @api.get("/schools/{schools_id}", response=SchoolSchema)
    def get_details_school(request, schools_id: int):

        school = get_object_or_404(Schools, pk=schools_id)

        return school

    @staticmethod
    @api.api_operation(["PUT", "POST"], "/schools/{schools_id}")
    def update_school(request, schools_id: int, payload: SchoolSchema):

        school, created = Schools.objects.get_or_create(pk=schools_id, defaults=payload.dict())
        school.title = payload.title
        school.save()

        return {"message": "success"}

    @staticmethod
    @api.delete("/schools/{schools_id}")
    def delete_school(request, schools_id: int):

        school = get_object_or_404(Schools, pk=schools_id)
        school.delete(SOFT_DELETE_CASCADE)

        return {"message": "success"}


class HeadMasterAPI:

    @staticmethod
    @api.get("/headmaster", response=list[HeadMasterSchemaOut])
    @paginate(LimitOffsetPagination)
    def get_list_headmaster(request):

        headmasters = Headmaster.objects.all()

        return headmasters

    @staticmethod
    @api.post("/headmaster")
    def create_headmaster(request, payload: HeadMasterSchemaIn):

        if school := Schools.objects.filter(pk=payload.school).first():
            payload.school = school
            headmaster = Headmaster.objects.create(**payload.dict())
        else:
            return api.create_response(request, {'message': "cannot find school."}, status=400)

        return {"id": headmaster.id}

    @staticmethod
    @api.get("/headmaster/{headmaster_id}", response=HeadMasterSchemaOut)
    def get_details_headmaster(request, headmaster_id: int):

        school = get_object_or_404(Headmaster, pk=headmaster_id)

        return school

    @staticmethod
    @api.patch("/headmaster/{headmaster_id}")
    def update_headmaster(request, headmaster_id: int, payload: HeadMasterSchemaIn):

        headmaster = get_object_or_404(Headmaster, pk=headmaster_id)
        headmaster.first_name = payload.first_name if payload.first_name else headmaster.first_name
        headmaster.last_name = payload.last_name if payload.last_name else headmaster.last_name

        if payload.school:
            school = Schools.objects.filter(pk=payload.school).first()
            payload.school = school
        else:
            payload.school = headmaster.school

        headmaster.school = payload.school
        headmaster.save()

        return {"message": "success"}

    @staticmethod
    @api.delete("/headmaster/{headmaster_id}")
    def delete_headmaster(request, headmaster_id: int):

        headmaster = get_object_or_404(Headmaster, pk=headmaster_id)
        headmaster.delete(SOFT_DELETE_CASCADE)

        return {"message": "success"}


class ClassAPI:

    @staticmethod
    @api.get("/class", response=list[ClassSchemaIn])
    @paginate(LimitOffsetPagination)
    def get_list_classroom(request):

        data = Class.objects.all()

        return data

    @staticmethod
    @api.post("/class")
    def create_classroom(request, payload: ClassSchemaOut):

        school = Schools.objects.filter(pk=payload.school).first()
        if school:
            payload.school = school
        else:
            return api.create_response(request, {"message": "cannot find school"}, status=400)

        new_class = Class(**payload.dict())
        new_class.full_clean()
        new_class.save()

        return {"id": new_class.id}

    @staticmethod
    @api.get("/class/{class_id}", response=ClassSchemaIn)
    def get_details_classroom(request, class_id: int):

        school = get_object_or_404(Class, pk=class_id)

        return school

    @staticmethod
    @api.patch("/class/{class_id}")
    def update_classroom(request, class_id: int, payload: ClassSchemaOut):

        classroom = get_object_or_404(Class, pk=class_id)
        classroom.title = payload.title if payload.title else classroom.title
        classroom.number_of_student = payload.number_of_student if payload.number_of_student else \
            classroom.number_of_student

        if school := Schools.objects.filter(pk=payload.school).first():
            payload.school = school
        else:
            payload.school = classroom.school

        classroom.school = payload.school
        classroom.save()

        return {"message": "success"}

    @staticmethod
    @api.delete("/class/{class_id}")
    def delete_classroom(request, class_id: int):

        classroom = get_object_or_404(Class, pk=class_id)
        classroom.delete(SOFT_DELETE_CASCADE)
        return {"message": "success"}


class StudentAPI:

    @staticmethod
    @api.get("/student", response=list[StudentSchemaOut])
    @paginate(LimitOffsetPagination)
    def get_list_student(request):

        data = Student.objects.all()

        return data

    @staticmethod
    @api.post("/student")
    def create_student(request, payload: StudentSchemaIn):

        classroom = Class.objects.filter(pk=payload.classroom).first()
        if Student.objects.filter(classroom=classroom, first_name=payload.first_name,
                                  last_name=payload.last_name).exists():
            return api.create_response(request, {"message": "Student already in this classroom."}, status=400)

        payload.classroom = classroom
        student = Student.objects.create(**payload.dict())

        return {"id": student.id}

    @staticmethod
    @api.get("/student/{student_id}", response=StudentSchemaOut)
    def get_details_student(request, student_id: int):

        student = get_object_or_404(Student, pk=student_id)
        return student

    @staticmethod
    @api.patch("/student/{student_id}")
    def update_student(request, student_id: int, payload: StudentSchemaIn):

        student = get_object_or_404(Student, pk=student_id)
        student.first_name = payload.first_name if payload.first_name else student.first_name
        student.last_name = payload.last_name if payload.last_name else \
            student.last_name
        student.student_id = payload.student_id if payload.student_id else student.student_id

        if classroom := Class.objects.filter(pk=payload.classroom).first():
            student.classroom = classroom
        else:
            student.classroom = student.classroom

        student.save()

        return {"message": "success"}

    @staticmethod
    @api.delete("/student/{student_id}")
    def delete_student(request, student_id: int):
        classroom = get_object_or_404(Student, pk=student_id)
        classroom.delete(SOFT_DELETE_CASCADE)
        return {"message": "success"}


class TeacherAPI:

    @staticmethod
    @api.get("/teacher", response=list[TeacherSchemaOut])
    @paginate(LimitOffsetPagination)
    def get_list_teacher(request):
        teachers = Teacher.objects.all()

        return teachers

    @staticmethod
    @api.post("/teacher")
    def create_teacher(request, payload: TeacherSchemaIn):
        classroom = Class.objects.filter(pk=payload.classroom).first()

        if Teacher.objects.filter(classroom=classroom, first_name=payload.first_name,
                                  last_name=payload.last_name).exists():
            return api.create_response(request, {"message": "Teacher already in this classroom."}, status=400)

        teacher = Teacher.objects.create(first_name=payload.first_name, last_name=payload.last_name,
                                         classroom=classroom if classroom else None)

        return {"id": teacher.id}

    @staticmethod
    @api.get("/teacher/{teacher_id}", response=TeacherSchemaOut)
    def get_details_teacher(request, teacher_id: int):

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        return teacher

    @staticmethod
    @api.patch("/teacher/{teacher_id}")
    def update_teacher(request, teacher_id: int, payload: TeacherSchemaIn):

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        teacher.first_name = payload.first_name if payload.first_name else teacher.first_name
        teacher.last_name = payload.last_name if payload.last_name else \
            teacher.last_name

        if classroom := Class.objects.filter(pk=payload.classroom).first():
            teacher.classroom = classroom
        else:
            teacher.classroom = teacher.classroom

        teacher.save()

        return {"message": "success"}

    @staticmethod
    @api.delete("/teacher/{teacher_id}")
    def delete_teacher(request, teacher_id: int):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        teacher.delete(SOFT_DELETE_CASCADE)
        return {"message": "success"}

