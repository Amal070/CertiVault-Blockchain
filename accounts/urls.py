from django.urls import path
from . import views

urlpatterns = [
    path('institution/register/', views.institute_register, name='institution_register'),
    path('institution/login/', views.institution_login, name='institution_login'),
    path('institution/dashboard/', views.institution_dashboard, name='institution_dashboard'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/verify-register-otp/', views.verify_student_register_otp, name='verify_student_register_otp'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile-update/', views.student_profile_update, name='student_profile_update'),
    path('student/enroll-course/', views.enroll_course, name='enroll_course'),
    path('logout/', views.user_logout, name='logout'),
]
