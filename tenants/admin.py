# from django.contrib import admin
# from django.conf import settings
# from django.db import connection

# # Register your models here.
# # لإدارة المستأجرين عبر لوحة تحكم Django:
# from .models import Client, Domain ,ClientSignupRequest
# # لا تسجل إلا إذا السكيما الحالية هي public
# # تسجل فقط إذا كنت في السكيما العامة
# if connection.schema_name == getattr(settings, "PUBLIC_SCHEMA_NAME", "public"):
#     admin.site.register(Client)
#     admin.site.register(Domain)
#     admin.site.register(ClientSignupRequest)


