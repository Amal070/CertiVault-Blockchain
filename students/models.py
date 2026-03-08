from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from institute.models import Institute, Course


# function to automatically store the current year during enrollment
def current_year():
    return timezone.now().year


class Student(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    student_id = models.CharField(
        max_length=50,
        unique=True
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    profile_photo = models.ImageField(
        upload_to="student_photos/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


class Enrollment(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    # automatically stores the year of enrollment
    course_year = models.IntegerField(
        default=current_year
    )

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_name}"


class CertificateRequest(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )

    certificate_name = models.CharField(
        max_length=200,
        help_text="Name to appear on certificate"
    )

    date_of_birth = models.DateField()

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):
        return f"{self.certificate_name} - {self.enrollment.course.course_name}"