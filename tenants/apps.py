from django.apps import AppConfig
from django.conf import settings
from django.db import connection


class TenantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'tenants'
    verbose_name = "Tenant Management"

    def ready(self):
        try:
            if connection.schema_name == getattr(settings, "PUBLIC_SCHEMA_NAME", "public"):
                from django.contrib import admin
                from .models import Client, Domain , ClientSignupRequest
                admin.site.register(Client)
                admin.site.register(Domain)
                admin.site.register(ClientSignupRequest)
        except Exception:
            # نتجاهل الأخطاء عند بدء التشغيل الأول
            pass

