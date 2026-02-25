from django.urls import path
from . import views

urlpatterns = [
    path('institution/register/', views.institution_register, name='institution_register'),
    path('institution/login/', views.institution_login, name='institution_login'),
    path('institution/dashboard/', views.institution_dashboard, name='institution_dashboard'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.user_logout, name='logout'),
]
