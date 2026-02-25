from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# ==========================
# INSTITUTION REGISTER
# ==========================
def institution_register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "accounts/institution_register.html", {
                "error": "Username already exists"
            })

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type="institution"
        )

        login(request, user)
        return redirect("institution_dashboard")

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
