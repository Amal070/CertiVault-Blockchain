from django.urls import path
from . import views

app_name = 'institute'

urlpatterns = [
    path('issue-certificate/', views.issue_certificate, name='issue_certificate'),
]
