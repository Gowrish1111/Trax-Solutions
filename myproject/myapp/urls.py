from django.urls import path
from . import views



urlpatterns = [
    path('students/bulk-create/',views.student_bulk_create),
    path('students/bulk-update/',views.student_bulk_update),

    path('courses/bulk-create/',views.course_bulk_create),
    path('courses/bulk-update/',views.course_bulk_update),

    path('trainers/', views.trainer_list),
    path('trainers/<int:trainer_id>/', views.trainer_detail),

    path('courses/', views.course_list),
    path('courses/<int:course_id>/', views.course_detail),

    path('enrollments/', views.enrollment_list),
    path('enrollments/<int:enrollment_id>/',views.enrollment_detail),

    path('assessments/', views.assessment_list),
    path('assessments/<int:assessment_id>/',views.assessment_detail),

    path('grades/', views.grade_list),
    path('grades/<int:grade_id>/',views.grade_detail),

    path('assessments/bulk-create/',views.assessment_bulk_create),
    path('assessments/bulk-update/',views.assessment_bulk_update),

    path('grades/bulk-create/',views.grade_bulk_create),
    path('grades/bulk-update/',views.grade_bulk_update),

    path('view-list/', views.view_list),

   
    path('login-page/', views.login_page),
    path('login/', views.login),
    path('student-dashboard/',views.student_dashboard),

    path(
    'student-dashboard-api/',
    views.student_dashboard_api,
    name='student_dashboard_api'
),
    
path(
    'dashboard/student/',
    views.student_dashboard_api_v2,
    name='student-dashboard-api-v2'
),
path(
    'dashboard/instructor/',
    views.instructor_dashboard_api_v2,
    name='instructor-dashboard-api-v2'
),

    
   
]