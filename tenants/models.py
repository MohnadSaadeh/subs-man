# Create your models here.
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    # schema_name = schema_name 
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    users_limit = models.IntegerField(default=3)
    on_trial = models.BooleanField(default=True)
    
    # الإعدادات الافتراضية لكل مستأجر
    auto_create_schema = True  # يقوم تلقائيًا بإنشاء المخطط  الجديد عند إضافة مستأجر

class Domain(DomainMixin):
    pass

#   شرح جدول الدومين
#   الي بالأعلى
# class Domain ():
#     domain = models.CharField(max_length=255)
#     tenant = models.ForeignKey('Client', on_delete=models.CASCADE)
#     is_primary = models.BooleanField(default=False)


# class TenantDomain(models.Model):
#     tenant = models.ForeignKey('Client', on_delete=models.CASCADE)
#     domain = models.CharField(max_length=255)

#     def __str__(self):
#         return self.domain

class ClientSignupRequest(models.Model):
    name = models.CharField(max_length=255)  # اسم المستأجر (النادي، الشركة، إلخ)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=100, help_text="نوع النشاط (رياضة، تعليم، إلخ)")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"