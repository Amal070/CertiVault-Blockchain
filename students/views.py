from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ==========================
# STUDENT DASHBOARD
# ==========================
@login_required
def student_dashboard(request):

    if request.user.user_type != "student":
        return redirect("students:student_login")

    # Import models
    from students.models import Student, Enrollment
    from institute.models import Institute, Course
    
    # Get or create student profile
    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            'student_id': f"STU{request.user.id}",
            'full_name': request.user.username,
            'email': request.user.email,
            'phone': "",
            'address': ""
        }
    )
    
    # Check if profile is incomplete
    profile_incomplete = not student.phone or not student.address
    
    # Get all institutes with their courses (show all for visibility)
    institutes = Institute.objects.all().prefetch_related('courses')
    
    # Get student's enrollments
    enrollments = Enrollment.objects.filter(student=student).select_related('institute', 'course').order_by('-created_at')
    
    # Get pending course requests
    pending_requests = enrollments.filter(status='Pending')
    
    # Get approved/completed courses
    active_courses = enrollments.filter(status='Approved')
    completed_courses = enrollments.filter(status='Completed')
    
    return render(request, "student/dashboard.html", {
        'student': student,
        'profile_incomplete': profile_incomplete,
        'institutes': institutes,
        'enrollments': enrollments,
        'pending_requests': pending_requests,
        'active_courses': active_courses,
        'completed_courses': completed_courses,
    })


# ==========================
# STUDENT PROFILE UPDATE
# ==========================
@login_required
def student_profile_update(request):
    if request.user.user_type != "student":
        return redirect("students:student_login")
    
    from students.models import Student
    
    student = Student.objects.get(user=request.user)
    
    if request.method == "POST":
        student.full_name = request.POST.get("full_name")
        student.phone = request.POST.get("phone")
        student.address = request.POST.get("address")
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("students:student_dashboard")
    
    return render(request, "student/profile_update.html", {"student": student})


# ==========================
# COURSE ENROLLMENT REQUEST
# ==========================
@login_required
def enroll_course(request):
    if request.user.user_type != "student":
        return redirect("students:student_login")
    
    if request.method == "POST":
        from students.models import Student, Enrollment
        from institute.models import Course
        
        course_id = request.POST.get("course_id")
        
        try:
            student = Student.objects.get(user=request.user)
            course = Course.objects.get(id=course_id)
            
            # Check if already enrolled
            if Enrollment.objects.filter(student=student, course=course).exists():
                messages.error(request, "You have already enrolled in this course!")
                return redirect("students:student_dashboard")
            
            # Create enrollment request
            Enrollment.objects.create(
                student=student,
                institute=course.institute,
                course=course,
                status="Pending"
            )
            
            messages.success(request, "Course enrollment request submitted! Wait for institute approval.")
            return redirect("students:student_dashboard")
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("students:student_dashboard")
    
    return redirect("students:student_dashboard")


# ==========================
# STUDENT LOGIN
# ==========================
def student_login(request):
    from django.contrib.auth import login, authenticate
    from accounts.models import CustomUser
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = CustomUser.objects.get(email=email, user_type='student')
            
            # Authenticate with username and password
            user = authenticate(request, username=student.username, password=password)

            if user is not None:
                login(request, user)
                return redirect("students:student_dashboard")
            else:
                return render(request, "student/login.html", {
                    "error": "Invalid password"
                })

        except CustomUser.DoesNotExist:

            return render(request,"student/login.html",
                          {"error":"Student account not found"})

    return render(request,"student/login.html")

