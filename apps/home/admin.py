# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import admin
from .models import *

admin.site.register(Classroom)
admin.site.register(Offer)
admin.site.register(Member)
admin.site.register(Subscription)
admin.site.register(Payment)

admin.site.site_header = "Subscriptions Manager"
admin.site.site_title = "Subscriptions Manager"
admin.site.index_title = "Welcome to Subscriptions Manager"



# Register your models here.
