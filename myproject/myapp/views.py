
from django.shortcuts import render,get_object_or_404
from django.db.models import Count
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Student,
    Course,
    Trainer,
    Enrollment,
    Assessment,
    Grade,
    Login,
)

from .serializers import (
    StudentSerializer,
    CourseSerializer,
    TrainerSerializer,
    EnrollmentSerializer,
    AssessmentSerializer,
    GradeSerializer,
)


# =========================================================
# LOGIN API
# POST /api/login/
# =========================================================

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not check_password(password, user.password):
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Safely access optional OneToOne relationships.
    student = getattr(user, 'student', None)
    trainer = getattr(user, 'trainer', None)

    return Response({
        'message': 'Login successful',
        'login_id': user.login_id,
        'username': user.username,
        'role': user.role,
        'student_id': student.student_id if student else None,
        'trainer_id': trainer.Trainer_id if trainer else None,
    })


# =========================================================
# STUDENT DASHBOARD - DJANGO HTML TEMPLATE
# GET /api/student-dashboard/?student_id=1
# =========================================================

def student_dashboard(request):
    student_id = request.GET.get('student_id')

    if not student_id:
        return render(
            request,
            'student_dashboard.html',
            {'error': 'Student ID not provided'}
        )

    try:
        student = Student.objects.get(student_id=student_id)
    except (Student.DoesNotExist, ValueError):
        return render(
            request,
            'student_dashboard.html',
            {'error': 'Student not found'}
        )

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related('course', 'course__trainer')

    grades = Grade.objects.filter(
        student=student
    ).select_related('assessment', 'assessment__course')

    return render(
        request,
        'student_dashboard.html',
        {
            'student': student,
            'enrollments': enrollments,
            'grades': grades,
        }
    )


# =========================================================
# STUDENT DASHBOARD - REACT JSON API
# GET /api/student-dashboard-api/?student_id=1
# =========================================================

@api_view(['GET'])
def student_dashboard_api(request):
    student_id = request.GET.get('student_id')

    if not student_id:
        return Response(
            {'error': 'Student ID not provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(student_id=student_id)
    except (Student.DoesNotExist, ValueError):
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related('course', 'course__trainer')

    grades = Grade.objects.filter(
        student=student
    ).select_related('assessment', 'assessment__course')

    # Include each course only once in the dashboard.
    courses_data = []
    seen_course_ids = set()

    for enrollment in enrollments:
        course = enrollment.course

        if course.course_id in seen_course_ids:
            continue

        seen_course_ids.add(course.course_id)
        trainer = course.trainer

        courses_data.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'trainer_name': (
                trainer.Trainer_name if trainer else 'Not assigned'
            ),
        })

    # Keep individual grade records so distinct assessments or
    # multiple grade records are not accidentally discarded.
    grades_data = []

    for grade in grades:
        assessment = grade.assessment

        grades_data.append({
            'grade_id': grade.grade_id,
            'assessment_id': assessment.assessment_id,
            'assessment_name': str(assessment),
            'course_name': assessment.course.course_name,
            'score': grade.score,
        })

    return Response({
        'student': {
            'student_id': student.student_id,
            'name': student.name,
            'email': student.email,
            'age': student.age,
        },
        'courses': courses_data,
        'grades': grades_data,
    })


# =========================================================
# STUDENT CRUD / BULK OPERATIONS
# =========================================================

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(StudentSerializer(student).data)

    if request.method == 'PUT':
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    student.delete()
    return Response(
        {'message': 'Student deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def student_bulk_create(request):
    serializer = StudentSerializer(data=request.data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
def student_bulk_update(request):
    if not isinstance(request.data, list):
        return Response(
            {'error': 'Expected a list of students.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    updated_students = []

    for student_data in request.data:
        student_id = student_data.get('student_id')

        try:
            student = Student.objects.get(student_id=student_id)
        except (Student.DoesNotExist, ValueError, TypeError):
            return Response(
                {'error': f'Student {student_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(
            student,
            data=student_data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        updated_students.append(serializer.data)

    return Response(updated_students)


# =========================================================
# COURSE CRUD / BULK OPERATIONS
# =========================================================

@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, course_id):
    try:
        course = Course.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(CourseSerializer(course).data)

    if request.method == 'PUT':
        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    course.delete()
    return Response(
        {'message': 'Course deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def course_bulk_create(request):
    serializer = CourseSerializer(data=request.data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
def course_bulk_update(request):
    if not isinstance(request.data, list):
        return Response(
            {'error': 'Expected a list of courses.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    updated_courses = []

    for course_data in request.data:
        course_id = course_data.get('course_id')

        try:
            course = Course.objects.get(course_id=course_id)
        except (Course.DoesNotExist, ValueError, TypeError):
            return Response(
                {'error': f'Course {course_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseSerializer(
            course,
            data=course_data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        updated_courses.append(serializer.data)

    return Response(updated_courses)


# =========================================================
# TRAINER CRUD
# =========================================================

@api_view(['GET', 'POST'])
def trainer_list(request):
    if request.method == 'GET':
        trainers = Trainer.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return Response(serializer.data)

    serializer = TrainerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def trainer_detail(request, trainer_id):
    try:
        trainer = Trainer.objects.get(Trainer_id=trainer_id)
    except Trainer.DoesNotExist:
        return Response(
            {'error': 'Trainer not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(TrainerSerializer(trainer).data)

    if request.method == 'PUT':
        serializer = TrainerSerializer(
            trainer,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    trainer.delete()
    return Response(
        {'message': 'Trainer deleted successfully'},
        status=status.HTTP_200_OK
    )


# =========================================================
# ENROLLMENT CRUD
# =========================================================

@api_view(['GET', 'POST'])
def enrollment_list(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    serializer = EnrollmentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def enrollment_detail(request, enrollment_id):
    try:
        enrollment = Enrollment.objects.get(
            enrollment_id=enrollment_id
        )
    except Enrollment.DoesNotExist:
        return Response(
            {'error': 'Enrollment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(EnrollmentSerializer(enrollment).data)

    if request.method == 'PUT':
        serializer = EnrollmentSerializer(
            enrollment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    enrollment.delete()
    return Response(
        {'message': 'Enrollment deleted successfully'},
        status=status.HTTP_200_OK
    )


# =========================================================
# ASSESSMENT CRUD / BULK OPERATIONS
# =========================================================

@api_view(['GET', 'POST'])
def assessment_list(request):
    if request.method == 'GET':
        assessments = Assessment.objects.all()
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data)

    serializer = AssessmentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def assessment_detail(request, assessment_id):
    try:
        assessment = Assessment.objects.get(
            assessment_id=assessment_id
        )
    except Assessment.DoesNotExist:
        return Response(
            {'error': 'Assessment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(AssessmentSerializer(assessment).data)

    if request.method == 'PUT':
        serializer = AssessmentSerializer(
            assessment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    assessment.delete()
    return Response(
        {'message': 'Assessment deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def assessment_bulk_create(request):
    serializer = AssessmentSerializer(data=request.data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
def assessment_bulk_update(request):
    if not isinstance(request.data, list):
        return Response(
            {'error': 'Expected a list of assessments.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    updated_assessments = []

    for assessment_data in request.data:
        assessment_id = assessment_data.get('assessment_id')

        try:
            assessment = Assessment.objects.get(
                assessment_id=assessment_id
            )
        except (Assessment.DoesNotExist, ValueError, TypeError):
            return Response(
                {'error': f'Assessment {assessment_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssessmentSerializer(
            assessment,
            data=assessment_data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        updated_assessments.append(serializer.data)

    return Response(updated_assessments)


# =========================================================
# GRADE CRUD / BULK OPERATIONS
# =========================================================

@api_view(['GET', 'POST'])
def grade_list(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    serializer = GradeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def grade_detail(request, grade_id):
    try:
        grade = Grade.objects.get(grade_id=grade_id)
    except Grade.DoesNotExist:
        return Response(
            {'error': 'Grade not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(GradeSerializer(grade).data)

    if request.method == 'PUT':
        serializer = GradeSerializer(
            grade,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    grade.delete()
    return Response(
        {'message': 'Grade deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def grade_bulk_create(request):
    serializer = GradeSerializer(data=request.data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
def grade_bulk_update(request):
    if not isinstance(request.data, list):
        return Response(
            {'error': 'Expected a list of grades.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    updated_grades = []

    for grade_data in request.data:
        grade_id = grade_data.get('grade_id')

        try:
            grade = Grade.objects.get(grade_id=grade_id)
        except (Grade.DoesNotExist, ValueError, TypeError):
            return Response(
                {'error': f'Grade {grade_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GradeSerializer(
            grade,
            data=grade_data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        updated_grades.append(serializer.data)

    return Response(updated_grades)


# =========================================================
# COURSE VIEW LIST - DJANGO HTML TEMPLATE
# =========================================================

def view_list(request):
    courses = Course.objects.select_related(
        'trainer'
    ).prefetch_related(
        'enrollment_set__student',
        'assessment_set__grade_set__student'
    ).annotate(
        student_count=Count(
            'enrollment__student',
            distinct=True
        ),
        assessment_count=Count(
            'assessment',
            distinct=True
        )
    )

    return render(
        request,
        'view_list.html',
        {'courses': courses}
    )


# =========================================================
# LOGIN PAGE - DJANGO HTML TEMPLATE
# =========================================================

def login_page(request):
    return render(request, 'login.html')




@api_view(['GET'])
def student_dashboard_api_v2(request):
    student_id = request.query_params.get('student_id')

    if not student_id:
        return Response(
            {"error": "student_id is required"},
            status=400
        )

    student = get_object_or_404(Student, student_id=student_id)

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related('course', 'course__trainer')

    courses = []
    seen_course_ids = set()

    for enrollment in enrollments:
        course = enrollment.course

        if course.course_id not in seen_course_ids:
            seen_course_ids.add(course.course_id)
            courses.append({
                "course_id": course.course_id,
                "course_name": course.course_name,
                "description": course.description,
                "start_date": course.start_date,
                "end_date": course.end_date,
                "trainer_name": (
                    course.trainer.Trainer_name
                    if course.trainer else None
                ),
            })

    grades_queryset = Grade.objects.filter(
        student=student
    ).select_related('assessment', 'assessment__course')

    grades = []
    for grade in grades_queryset:
        assessment = grade.assessment
        course = assessment.course

        grades.append({
            "grade_id": grade.grade_id,
            "assessment_id": assessment.assessment_id,
            "assessment_name": assessment.title,
            "assessment_type": assessment.assessment_type,
            "course_id": course.course_id,
            "course_name": course.course_name,
            "score": grade.score,
            "max_score": assessment.max_score,
            "percentage": round(
                (grade.score / assessment.max_score) * 100, 2
            ) if assessment.max_score else None,
        })

    average_percentage = (
        round(
            sum(g["percentage"] for g in grades if g["percentage"] is not None)
            / sum(1 for g in grades if g["percentage"] is not None),
            2
        )
        if any(g["percentage"] is not None for g in grades)
        else 0
    )

    return Response({
        "student": {
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "dob": student.dob,
        },
        "stats": {
            "course_count": len(courses),
            "assessment_count": len(grades),
            "average_score_percentage": average_percentage,
        },
        "courses": courses,
        "grades": grades,
    })




@api_view(['GET'])
def instructor_dashboard_api_v2(request):
    trainer_id = request.query_params.get('trainer_id')

    if not trainer_id:
        return Response(
            {"error": "trainer_id is required"},
            status=400
        )

    trainer = get_object_or_404(Trainer, Trainer_id=trainer_id)

    assigned_courses = Course.objects.filter(
        trainer=trainer
    ).order_by('course_name')

    courses = []
    course_ids = list(
        assigned_courses.values_list('course_id', flat=True)
    )

    for course in assigned_courses:
        student_count = Enrollment.objects.filter(
            course=course
        ).values('student_id').distinct().count()

        assessment_count = Assessment.objects.filter(
            course=course
        ).count()

        courses.append({
            "course_id": course.course_id,
            "course_name": course.course_name,
            "description": course.description,
            "start_date": course.start_date,
            "end_date": course.end_date,
            "capacity": course.capacity,
            "student_count": student_count,
            "assessment_count": assessment_count,
        })

    enrolled_student_ids = Enrollment.objects.filter(
        course_id__in=course_ids
    ).values_list('student_id', flat=True).distinct()

    assessments_queryset = Assessment.objects.filter(
        course_id__in=course_ids
    ).select_related('course').order_by('course__course_name', 'title')

    assessments = []

    for assessment in assessments_queryset:
        assessment_grades = Grade.objects.filter(
            assessment=assessment
        ).select_related('student').order_by('student__name')

        assessments.append({
            "assessment_id": assessment.assessment_id,
            "title": assessment.title,
            "assessment_type": assessment.assessment_type,
            "description": assessment.description,
            "course_id": assessment.course.course_id,
            "course_name": assessment.course.course_name,
            "max_score": assessment.max_score,
            "created_date": assessment.created_date,
            "grades": [
                {
                    "grade_id": grade.grade_id,
                    "student_id": grade.student.student_id,
                    "student_name": grade.student.name,
                    "score": grade.score,
                    "percentage": round(
                        (grade.score / assessment.max_score) * 100, 2
                    ) if assessment.max_score else None,
                }
                for grade in assessment_grades
            ],
        })

    return Response({
        "trainer": {
            "trainer_id": trainer.Trainer_id,
            "name": trainer.Trainer_name,
            "email": trainer.email,
            "department": trainer.dept,
        },
        "stats": {
            "course_count": len(courses),
            "student_count": len(enrolled_student_ids),
            "assessment_count": len(assessments),
        },
        "courses": courses,
        "assessments": assessments,
    })
