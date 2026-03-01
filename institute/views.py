import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Certificate
from blockchain.utils import store_hash_on_blockchain


@login_required
def upload_certificate(request):

    if request.user.user_type != "institution":
        return redirect("login")

    if request.method == "POST":

        certificate_file = request.FILES.get("certificate_file")
        student_name = request.POST.get("student_name")
        register_number = request.POST.get("register_number")
        course = request.POST.get("course")
        year_of_passing = request.POST.get("year_of_passing")

        # Generate SHA256 hash
        file_data = certificate_file.read()
        hash_value = hashlib.sha256(file_data).hexdigest()

        certificate_file.seek(0)

        # Prevent duplicate
        if Certificate.objects.filter(certificate_hash=hash_value).exists():
            messages.error(request, "Certificate already exists.")
            return redirect("upload_certificate")

        # Store on Blockchain
        try:
            tx_hash = store_hash_on_blockchain(hash_value)
        except Exception as e:
            messages.error(request, f"Blockchain Error: {str(e)}")
            return redirect("upload_certificate")

        # Save in DB
        Certificate.objects.create(
            student_name=student_name,
            register_number=register_number,
            course=course,
            year_of_passing=year_of_passing,
            issued_by=request.user,
            certificate_file=certificate_file,
            certificate_hash=hash_value,
            blockchain_tx_hash=tx_hash
        )

        messages.success(request, "Certificate stored on blockchain successfully.")
        return redirect("institution_dashboard")

    return render(request, "institute/upload_certificate.html")