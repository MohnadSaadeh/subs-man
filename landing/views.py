from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientSignupForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# from .models import ClientSignupRequest
from tenants.models import Client , ClientSignupRequest ,Domain# استيراد نموذج المستأجر
from django.db import models

def landing_page(request):
    # if request.method == 'POST':
    #     form = ClientSignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, ' تم إرسال طلبك بنجاح، سيتم مراجعته قريبًا.') #Your request has been submitted successfully!
    #         return redirect('landing_page')
    # else:
    #     form = ClientSignupForm()

    return render(request, 'landing/landing_page.html')


def signup(request):
    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' تم إرسال طلبك بنجاح، سيتم مراجعته قريبًا.') #Your request has been submitted successfully!
            return redirect('landing_page')
    else:
        form = ClientSignupForm()

    return render(request, 'landing/signup.html', {'form': form})

@login_required(login_url='/admin')
def admin_review_requests(request):
    # if not request.user.is_authenticated:
    #     return redirect('landing_page')  # Redirect to landing page if not logged in
    pinding_requests = ClientSignupRequest.objects.filter(status='pending')
    return render(request, 'landing/admin_review.html', {'requests': pinding_requests})

@login_required
def approve_request(request, request_id):
    signup_request = get_object_or_404(ClientSignupRequest, id=request_id)
    signup_request.status = "approved"
    signup_request.save()

    # إنشاء مستأجر جديد تلقائيًا بعد الموافقة
    # Client.objects.create(name=signup_request.name, schema_name=signup_request.name.lower().replace(" ", "_"))
    Client.objects.create(name=signup_request.name, paid_until="2025-12-31", on_trial=True, schema_name=signup_request.name.lower().replace(" ", "_"))
    tenant = Client.objects.get(name=signup_request.name)
    tenant_domain = signup_request.name.lower().replace(" ", "_")
    # إنشاء النطاق المرتبط بالمستأجر
    Domain.objects.create(domain=f"{tenant_domain}.localhost", tenant=tenant)

    return redirect('admin_review_requests')