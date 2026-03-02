import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import InstituteCertificate
from .forms import InstituteCertificateForm
from blockchain.utils import store_hash_on_blockchain


@login_required
def issue_certificate(request):

    if request.user.user_type != "institution":
        return redirect("institution_login")

    if request.method == "POST":
        form = InstituteCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert_file = form.cleaned_data['certificate_file']

            # Compute SHA256 using chunks to avoid large memory spikes
            sha = hashlib.sha256()
            for chunk in cert_file.chunks():
                sha.update(chunk)
            hash_value = sha.hexdigest()

            # Reset file pointer so saving works correctly
            try:
                cert_file.seek(0)
            except Exception:
                pass

            # Prevent duplicate hash
            if InstituteCertificate.objects.filter(certificate_hash=hash_value).exists():
                messages.error(request, "Certificate with same content already issued.")
                return redirect("issue_certificate")

            # Store on blockchain
            try:
                tx_hash = store_hash_on_blockchain(hash_value)
            except Exception as e:
                messages.error(request, f"Blockchain error: {str(e)}")
                return redirect("issue_certificate")

            # Save record
            try:
                inst_cert = form.save(commit=False)
                inst_cert.institute = request.user
                inst_cert.certificate_hash = hash_value
                inst_cert.blockchain_tx_hash = tx_hash
                inst_cert.save()
            except IntegrityError:
                messages.error(request, "Duplicate certificate hash detected.")
                return redirect("issue_certificate")

            messages.success(request, "Certificate issued and stored on blockchain.")
            return redirect("institution_dashboard")
    else:
        # Prefill form if register_number provided and exists for this institute
        reg_no = request.GET.get('register_number')
        initial = None
        if reg_no:
            existing = InstituteCertificate.objects.filter(institute=request.user, register_number=reg_no).first()
            if existing:
                initial = {
                    'student_name': existing.student_name,
                    'student_email': existing.student_email,
                    'course': existing.course,
                    'year_of_passing': existing.year_of_passing,
                    'register_number': existing.register_number,
                }

        form = InstituteCertificateForm(initial=initial)

    return render(request, "institute/issue_certificate.html", {"form": form})