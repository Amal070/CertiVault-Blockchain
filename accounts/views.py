from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from institute.models import Institute


# ==========================
# INSTITUTION REGISTER
# ==========================
def institute_register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        institute_name = request.POST.get("institute_name")
        institute_code = request.POST.get("institute_code")
        affiliation = request.POST.get("affiliation")
        type_inst = request.POST.get("type")
        established_year = request.POST.get("established_year")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        website = request.POST.get("website")
        address = request.POST.get("address")
        admin_name = request.POST.get("admin_name")
        designation = request.POST.get("designation")
        govt_reg_no = request.POST.get("govt_reg_no")
        accreditation = request.POST.get("accreditation")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("institute_register")

        # Create login account
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            user_type="institution"
        )

        # Create institute profile
        Institute.objects.create(
            user=user,
            institute_name=institute_name,
            institute_code=institute_code,
            affiliation=affiliation,
            type=type_inst,
            established_year=established_year,
            email=email,
            phone=phone,
            website=website,
            address=address,
            admin_name=admin_name,
            designation=designation,
            govt_reg_no=govt_reg_no,
            accreditation=accreditation,
            authorization_file=request.FILES.get("authorization_file"),
            logo=request.FILES.get("logo"),
        )

        messages.success(request, "Registration submitted. Wait for approval.")
        return redirect("login")

    return render(request, "accounts/institution_register.html")

# ==========================
# INSTITUTION LOGIN
# ==========================
def institution_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == "institution":
            login(request, user)
            return redirect("institution_dashboard")
        else:
            return render(request, "accounts/institution_login.html", {
                "error": "Invalid credentials or not an Institution"
            })

    return render(request, "accounts/institution_login.html")


# ==========================
# INSTITUTION DASHBOARD
# ==========================
@login_required
def institution_dashboard(request):

    if request.user.user_type != "institution":
        return redirect("institution_login")

    return render(request, "institute/institution_dashboard.html")


# ==========================
# USER REGISTER
# ==========================
def user_register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "accounts/user_register.html", {
                "error": "Username already exists"
            })

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type="user"
        )

        login(request, user)
        return redirect("user_dashboard")

    return render(request, "accounts/user_register.html")


# ==========================
# USER LOGIN
# ==========================
def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == "user":
            login(request, user)
            return redirect("user_dashboard")
        else:
            return render(request, "accounts/user_login.html", {
                "error": "Invalid credentials or not a User"
            })

    return render(request, "accounts/user_login.html")


# ==========================
# USER DASHBOARD
# ==========================
@login_required
def user_dashboard(request):

    if request.user.user_type != "user":
        return redirect("user_login")

    return render(request, "users/user_dashboard.html")


# ==========================
# LOGOUT
# ==========================
def user_logout(request):
    logout(request)
    return redirect("/")
