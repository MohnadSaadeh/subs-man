# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.auth import views as auth_views




urlpatterns = [

    path('sign-up', views.sign_up, name ='sign_up'),

    path('dashboard', views.index, name='home'),
    path('', views.index),
    # path('login', views.login_page), #page


    # path('login_user', views.login_user), #function

    path('logout', views.logout_user),
    
    # Matches any html file     
    re_path(r'^home.*', views.pages, name='pages'),#re_path(r'^.*\.*', views.pages, name='pages'),
    path('add_class_page', views.add_class_page),
    path('add_class', views.add_class),
    path('view_calss_page', views.view_calss_page),

    path('add_offer_page', views.add_offer_page),
    path('add_offer', views.     add_offer),
    # path('view_subs_type', views.    view_subs_type_page),

    path('add_member_page', views.add_member_page),
    path('add_member', views.     add_member),

    path('view_class/<int:id>', views.enter_a_class),

    # path('subscribe_a_member/', views.subscribe_a_member, name='subscribe_a_member'),

    path('subscribe/<int:id>/', views.subscribe_a_member,  name='subscribe_a_member_with_id'),

    path('member_profile/<int:id>', views.enter_member_profile),

    path("process-payment/", views.process_payment, name="process_payment"),#sub Payment

    path('expired_subscriptions', views.expired_subscriptions),


    

    path('register', views.register, name='register ') ,
    # path('registeration', views.registeration)



]
