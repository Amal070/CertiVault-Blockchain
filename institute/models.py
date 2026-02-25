from django.db import models
from django.conf import settings

class InstituteProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.institute_name


class Certificate(models.Model):
    student_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')
    certificate_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name