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

    # import inside to avoid circular at module load
    from institute.forms import InstituteCertificateForm
    from institute.models import InstituteCertificate
    from blockchain.utils import store_hash_on_blockchain, verify_hash_from_blockchain
    import hashlib
    from django.db import IntegrityError

    # statistics
    total_issued = InstituteCertificate.objects.filter(institute=request.user).count()
    # placeholder values for pending/verified; adjust if you add status fields later
    pending = 0
    verified = 0

    form = InstituteCertificateForm()

    if request.method == "POST":
        form = InstituteCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert_file = form.cleaned_data['certificate_file']
            sha = hashlib.sha256()
            for chunk in cert_file.chunks():
                sha.update(chunk)
            hash_value = sha.hexdigest()
            try:
                cert_file.seek(0)
            except Exception:
                pass

            if InstituteCertificate.objects.filter(certificate_hash=hash_value).exists():
                messages.error(request, "Certificate with same content already issued.")
                return redirect("institution_dashboard")

            try:
                tx_hash = store_hash_on_blockchain(hash_value)
            except Exception as e:
                messages.error(request, f"Blockchain error: {str(e)}")
                return redirect("institution_dashboard")

            # verify immediately after sending
            verified = False
            try:
                verified = verify_hash_from_blockchain(hash_value)
            except Exception:
                # if verify call fails we'll still record but mark unverified
                verified = False

            try:
                inst_cert = form.save(commit=False)
                inst_cert.institute = request.user
                inst_cert.certificate_hash = hash_value
                inst_cert.blockchain_tx_hash = tx_hash
                inst_cert.save()
            except IntegrityError:
                messages.error(request, "Duplicate certificate hash detected.")
                return redirect("institution_dashboard")

            request.session['last_tx_hash'] = tx_hash
            request.session['last_verified'] = verified
            messages.success(request, "Certificate issued and stored on blockchain.")
            return redirect("institution_dashboard")

    # pull tx hash and verification status from session if available
    last_tx = request.session.pop('last_tx_hash', None)
    last_verified = request.session.pop('last_verified', None)
    return render(request, "institute/institution_dashboard.html", {
        "form": form,
        "total_issued": total_issued,
        "pending": pending,
        "verified": verified,
        "last_tx_hash": last_tx,
        "last_verified": last_verified,
    })


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

    # Import blockchain functions here to avoid import errors
    from blockchain.utils import verify_hash_from_blockchain
    from institute.models import Certificate
    from users.models import VerificationHistory
    import hashlib

    result = None
    certificate_data = None

    if request.method == "POST":

        certificate_file = request.FILES.get("certificate")

        if certificate_file:

            # Generate SHA256 hash
            file_data = certificate_file.read()
            hash_value = hashlib.sha256(file_data).hexdigest()
            certificate_file.seek(0)

            try:
                # Verify from blockchain
                is_valid = verify_hash_from_blockchain(hash_value)

                if is_valid:
                    result = "VALID"

                    # Fetch certificate details
                    certificate_data = Certificate.objects.filter(
                        certificate_hash=hash_value
                    ).first()

                else:
                    result = "INVALID"

                # Save verification history
                VerificationHistory.objects.create(
                    user=request.user,
                    certificate_id=hash_value,
                    result=result
                )

            except Exception as e:
                error_msg = str(e)
                # Check if it's a connection error
                if "connection" in error_msg.lower() or "refused" in error_msg.lower():
                    result = "⚠️ Blockchain not connected. Please start Ganache to verify certificates."
                else:
                    result = f"Blockchain Error: {error_msg}"

    return render(request, "users/user_dashboard.html", {
        "result": result,
        "certificate": certificate_data
    })


# ==========================
# LOGOUT
# ==========================
def user_logout(request):
    logout(request)
    return redirect("/")
