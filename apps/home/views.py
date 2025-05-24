# # -*- encoding: utf-8 -*-
# """
# Copyright (c) 2019 - present AppSeed.us
# """

# from django import template
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse


# @login_required(login_url="/login/")
# def index(request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))






# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse

# def index(request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))






from django.http import HttpResponse, HttpResponseRedirect 
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render , redirect
from . import models
from django.contrib import messages
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from apps.home.models import Member ,  Subscription , Payment ,Notification 
from django.views.decorators.csrf import csrf_exempt #payment
import json #payment
from decimal import Decimal #payment
from datetime import date
from django.core.paginator import Paginator #page     #  لتقسيم النتائج إلى صفحات تحتوي على 10 عناصر
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from apps.home.forms import RegisterForm 
from django.utils.http import urlencode
from datetime import date
import requests
from django.conf import settings
from django.utils.translation import gettext as _
from urllib.parse import quote # WhatsApp

# def sign_up(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # user table size
#             if User.objects.count() >= 3:
#                 messages.error(request, 'Maximum number of users reached. Please contact the administrator.')
#                 return render(request, 'registration/sign_up.html', {'form': form})
#             user = form.save()

#             login(request, user)
#             return redirect('/dashboard')
#     else: #validate
#         form = RegisterForm()
#     return render(request, 'registration/sign_up.html', {'form': form})
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # user table size
            if User.objects.count() >= request.tenant.users_limit: # users_limit in Tenant model
                return render(request, 'registration/sign_up.html', {
                    'form': form ,
                    # 'limit_exceeded': True
                    'error_message': _('Opps , You have exceeded the limit of active users for this organization.')
                    })
            user = form.save()
            login(request, user) #if you want to log in directly
            return redirect('/dashboard')
    else: #validate
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})



# def registeration(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['pass']
#         email = request.POST['email']
#         user = User.objects.create_user(username=username, password=password, email=email)
#         user.save()
#         return redirect('/login')
#     return render(request, 'home/register.html')



# the dashboard 
# if we not loged in redirecy to login
@login_required(login_url="/login")
def index(request):
    offers = models.get_all_offers()
    members = models.get_all_members()
    classes = models.get_all_classrooms()
    context = {
        'segment': index,
        'offers': offers,
        'members' : members,
        'classes' : classes,
        }
    
    return render(request, 'home/index.html', context)

    # html_template = loader.get_template('home/index.html')
    # return HttpResponse(html_template.render(context, request))

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print("logged in ACCEPTED")
#             return redirect('/dashboard')
#             # return render (request, 'home/index.html')
            
#         else:
#             messages.error(request, 'Invalid username or password')
#     return render(request, 'home/login.html')

def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required(login_url="/login")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    try:
        
        load_template = request.path.split('/')[-1]
        
        context['segment'] = load_template
        
        html_template = loader.get_template('home/' + load_template)
        
        
        
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def login_page(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/login.html')
    return HttpResponse(html_template.render(context, request))

def register(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/register.html')
    return HttpResponse(html_template.render(context, request))
    



def add_class_page(request):
    return render(request, 'home/page-class.html')

def add_class(request):
    name = request.POST['classname']
    description = request.POST['description']
    dayofweek = request.POST['dayofweek']
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']
    models.create_classroom(name,description,dayofweek,starttime,endtime)
    return redirect('/')

def view_calss_page(request):
    classes = models.get_all_classrooms()
    context = {
        'classes': classes ,
        'segment' : 'ui-tables'  # makes the div active when you click
        }
    return render(request, 'home/ui-tables.html', context)



def add_offer_page(request):
    return render(request, 'home/page-offer.html')
def add_offer(request):
    offer_name = request.POST['offer_name']
    description = request.POST['offer_description'] 
    price = request.POST['offer_price'] 
    duration_months = request.POST['duration_months']
    models.create_offer(offer_name, description, price, duration_months)
    return redirect('/')

def add_member_page(request):
    context = {
        'classes' : models.get_all_classrooms(),  
    }
    return render(request, 'add/add-member-page.html', context)
def add_member(request):
    
    name = request.POST['name']
    phone = request.POST['phoneNumber']
    email = request.POST['email']
    classID = request.POST['classID'] #need class_id after
    print(classID)
    models.create_member(name, phone, email, classID)
    return redirect('/')

def enter_a_class(request, id):
    today = date.today() # Get today's date
    # Fetch all members in the class
    members = models.get_classroom_members(id).order_by ('updated_at','id')
    # Update status for each member
    for member in members:
        subscriptions = Subscription.objects.filter(member=member)
#         msg = f"""مرحبًا {member.name} 👋

#  نود تذكيرك بأن اليوم {date.today()} في 🏋️‍♂️ {member.class_name}  
# ان الحصه على موعدها💪

# شكراً لك!
# """




        # تحديد اسم اليوم الحالي بالإنجليزية
        today = datetime.date.today()
        english_day_name = today.strftime('%A')

        # ترجمة اسم اليوم إلى العربية
        days_translation = {
            'Monday': 'الاثنين',
            'Tuesday': 'الثلاثاء',
            'Wednesday': 'الأربعاء',
            'Thursday': 'الخميس',
            'Friday': 'الجمعة',
            'Saturday': 'السبت',
            'Sunday': 'الأحد',
        }
        arabic_day_name = days_translation[english_day_name]

        # الرسالة
        msg = f"""مرحبًا 
        {member.name} 
نود تذكيرك بأن اليوم { arabic_day_name}
{date.today() }   
{member.class_name} في  
ان الحصه على موعدها💪

شكراً لك!
"""

        member.encoded_message = quote(msg, safe='')
        for subscription in subscriptions:
            if subscription.end_date >= date.today() and member.balance == 0:
                member.status = 'active'
            elif subscription.end_date >= date.today() and member.balance > 0:
                member.status = 'overdue'
            elif subscription.end_date < date.today() and member.balance > 0:
                member.status = 'suspended'
            else:
                member.status = 'expired'
            member.save()

    context = {
        'class' : models.get_classroom(id),
        'members' : members ,
        'offers' : models.get_all_offers(),
        'today': today,
    }
    return render(request, 'home/page-inside-a-class.html',context)


def subscribe_a_member(request ,id):
    errors = models.Subscription.objects.Subscription_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     # #return redirect(f'/view_class/{id}') 
    if errors:
        return JsonResponse({'status': 'error', 'errors': errors})  ## Return JSON for errors

    else:
    
        member_id = models.get_member_id(id=id)
        class_id = models.get_classroom_id_from_member(member_id = id)#Fix variable
        # print(member_id) #name
        print(f"member id {id}") #mem id 1
        print(f"in class id {class_id}" ) 
        offer_id = request.POST['offerID']
        # start_date = request.POST['start_date']
        start_date = datetime.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        # end_date =  request.POST['end_date']
        end_date = datetime.datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        # free_days = request.POST['free_days']
        free_days = int(request.POST['free_days'])  # Convert to integer
        descount =  request.POST['descount']
        # Calculate new end_date including free days
        end_date_after_free_days = end_date + datetime.timedelta(days=free_days)
        subscribe = models.create_subscription(member_id, offer_id , start_date, end_date_after_free_days, free_days, descount)
        if subscribe:
            print(end_date_after_free_days)
            #########################################
            models.update_member_balance(id)
            #########################################
            # models.create_payment(subscribe, 0, 'CASH')
            print(f"Subscription successful for member {member_id}") 
            return JsonResponse({'status': 'success', 'message': "Successfully added a Subscription!", 'class_id': class_id})
            
        return JsonResponse({'status': 'error', 'message': "Subscription failed"}, status=400)

        
def enter_member_profile(request, id):
    today = date.today() # Get today's date
    member  = get_object_or_404(Member, id=id)
    subscriptions = member.subscriptions.all().order_by('-start_date')
    final_balance = member.balance
    context = {
        'member' : member,
        'subscriptions' : subscriptions,
        'final_balance' : final_balance,
        'today': today,
    }
    return render(request, 'home/page-member-profile.html',context )

@csrf_exempt  # If using CSRF, remove this and handle CSRF properly
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            member_id = data.get("member_id")
            subscription_id = data.get("subscription_id")
            amount = data.get("amount")

            if not (member_id and subscription_id and amount):
                return JsonResponse({"message": "Missing required fields"}, status=400)
            
            # Convert amount to Decimal to avoid type error
            try:
                amount = Decimal(amount)
            except ValueError:
                # return JsonResponse({"message": "Invalid amount format"}, status=400)
                return JsonResponse({"message": _("Missing required fields")}, status=400)


            # Validate member and subscription
            try:
                member = Member.objects.get(id=member_id)
                subscription = Subscription.objects.get(id=subscription_id, member=member)
                # cannot pay more than the subscriptoin
                if amount > subscription.remaining_balance:
                    return JsonResponse({"message": "Amount exceeds remaining balance"}, status=400)
                
            except (Member.DoesNotExist, Subscription.DoesNotExist):
                return JsonResponse({"message": "Invalid member or subscription"}, status=404)

            #Save payment
            Payment.objects.create(
                member=member,
                subscription=subscription,
                amount_paid=amount
            )
            amount = data.get("amount")
            print("Received Data:", data)

            return JsonResponse({"success": True, "message": "Payment successful"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=405)

@login_required(login_url="/login")
def expired_subscriptions (request):
    expired_member_subscriptions = models.get_expired_subscriptions()
    
    # إعداد الPaginator لتقسيم النتائج إلى صفحات تحتوي على 10 عناصر
    paginator = Paginator(expired_member_subscriptions, 10)  # 10 هو عدد العناصر في كل صفحة
    
    # الحصول على الرقم الحالي للصفحة من استعلام GET (إذا لم يكن موجودًا، سيتم تعيينه إلى 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    for member in page_obj:
        msg = f"""مرحبًا {member.name} 👋

نود تذكيرك بأن اشتراكك في 🏋️‍♂️ {member.class_name} 
قد **انتهى**.
يرجى التجديد في أقرب وقت للاستفادة من خدماتنا والاستمرار في التقدم 💪

شكراً لك!
"""

        member.encoded_message = quote(msg, safe='')






    context = {
        'page_obj': page_obj,
        'expired_subscriptions' : expired_subscriptions,
        'segment' : 'ui-tables'  # makes the div active when you click
        }
    return render(request, 'subs_status/expired.html', context)






# def expired_subscriptions(request):
#     expired_member_subscriptions = models.get_expired_subscriptions()
#     for member in expired_member_subscriptions:
#         msg = f"""مرحبًا {member.name} 👋

# نود تذكيرك بأن اشتراكك في 🏋️‍♂️ {member.class_name} 
# قد **انتهى**.
# يرجى التجديد في أقرب وقت للاستفادة من خدماتنا والاستمرار في التقدم 💪

# شكراً لك!
# """

#         member.encoded_message = quote(msg, safe='')
#     context = {
#         'page_obj': expired_member_subscriptions,
#     }
#     return render(request, 'subs_status/expired.html', context)









