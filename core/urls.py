# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.i18n import i18n_patterns  #translation
from django.views.i18n import set_language
# from django.conf.urls import url
from django.conf import settings



urlpatterns = [ 	 
        path('set-language/', set_language, name='set_language'),  # << هذا مهم

        path('admin/', admin.site.urls),
        # path('dashboard', include("apps.home.urls")),  
        path('', include("apps.home.urls")), 
        #New app include all the app urls
        # path('', include('landing.urls')),  # صفحة الهبوط
        #login , logout , password-reset  ,.....
        path('', include('django.contrib.auth.urls' ) ),
    ] 

