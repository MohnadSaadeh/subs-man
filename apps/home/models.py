# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validations import SubscriptionManager #valedate
from django.utils import timezone
from django.db.models import Subquery, OuterRef
from django.contrib.auth.models import AbstractUser
#for translation
from django.utils.translation import gettext_lazy as _  

# class CustomUser(AbstractUser):
#     users_limit = models.IntegerField(default=3)  # Set the default limit to 3 





class Classroom(models.Model): # i will call it ActivityRoom i  the future
    name = models.CharField(max_length=100)
    description = models.TextField()
    day_of_week = models.CharField(max_length=10)  # مثل "Monday", "Tuesday", etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #members
    def __str__(self):
        return self.name

# class Classroom(models.Model):  # i will call it ActivityRoom i  the future
#     name = models.CharField(max_length=100, verbose_name=_("Room Name"))
#     description = models.TextField(verbose_name=_("Description"))
#     day_of_week = models.CharField(max_length=10, verbose_name=_("Day of Week"))  # مثل Monday
#     start_time = models.TimeField(verbose_name=_("Start Time"))
#     end_time = models.TimeField(verbose_name=_("End Time"))
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

#     def __str__(self):
#         return self.name



class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #subscriptions
    #members
    def __str__(self):
        return self.offer_name

# Offers 1 month  or 3 monthes or 12 monthes
# class Offer(models.Model):
#     offer_name = models.CharField(max_length=100, verbose_name=_("Offer Name"))
#     description = models.TextField(verbose_name=_("Description"))
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
#     duration_months = models.IntegerField(verbose_name=_("Duration (Months)"))
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

#     def __str__(self):
#         return self.offer_name


class Member(models.Model):
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('expired', 'منتهي الاشتراك'),
        ('overdue', 'متأخر في الدفع'),
        ('suspended', 'مجمّد'),
        ('banned', 'محظور'),
        ('new', 'جديد'),
    ]
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    class_name = models.ForeignKey(Classroom, on_delete=models.SET_DEFAULT , default='No Class' , related_name='members') # relarelated_name is optional you can use member_set
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')###########
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  #join_date     # auto_now_add=True value not changed after first ceretion
    updated_at = models.DateTimeField(auto_now=True)
    #subscriptions
    ######################### New ############################
    def get_latest_subscription(self):
        return self.subscriptions.order_by('-id').first()

    def __str__(self):
        return self.name

# class Member(models.Model):
#     STATUS_CHOICES = [
#         ('active', _("Active")),
#         ('expired', _("Expired")),
#         ('overdue', _("Overdue")),
#         ('suspended', _("Suspended")),
#         ('banned', _("Banned")),
#         ('new', _("New")),
#     ]
#     name = models.CharField(max_length=100, verbose_name=_("Full Name"))
#     phone_number = models.CharField(max_length=15, verbose_name=_("Phone Number"))
#     email = models.EmailField(unique=True, verbose_name=_("Email"))
#     class_name = models.ForeignKey(
#         Classroom,
#         on_delete=models.SET_DEFAULT,
#         default='No Class',
#         related_name='members',
#         verbose_name=_("Classroom")
#     )
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Balance"))
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name=_("Status"))
#     is_free = models.BooleanField(default=False, verbose_name=_("Free Member"))
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Join Date"))
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

#     def get_latest_subscription(self):
#         return self.subscriptions.order_by('-id').first()

#     def __str__(self):
#         return self.name



# #يحتوي على معلومات الاشتراكات وطريقة الدفع (كامل أو أقساط).
class Subscription(models.Model):
    #if the offer is deleted the offer value will be the first  aded 
    def get_default_offers():
        return Offer.objects.first() if Offer.objects.exists() else None 

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name = 'subscriptions' ,null = True )
    offer =      models.ForeignKey(Offer, on_delete=models.SET_DEFAULT, default=get_default_offers, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    free_days = models.IntegerField(default=0)  # عدد الأيام المجانية
    descount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # الخصم
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    objects = SubscriptionManager() #from validation.py    

    def save(self, *args, **kwargs):
        self.is_active = not self.is_expired()
        # Set initial remaining_balance to the Offer's price if not already set when the instance is being created 
        if self._state.adding and not self.remaining_balance:
            self.remaining_balance = self.offer.price
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.end_date < timezone.now().date()
        
    def __str__(self):
        return f"{self.member.name} - {self.start_date} to {self.end_date}"

# # #يحتوي على معلومات الاشتراكات وطريقة الدفع (كامل أو أقساط).
# class Subscription(models.Model):
#     def get_default_offers():
#         return Offer.objects.first() if Offer.objects.exists() else None 

#     member = models.ForeignKey(
#         Member, on_delete=models.CASCADE, related_name='subscriptions', null=True, verbose_name=_("Member")
#     )
#     offer = models.ForeignKey(
#         Offer,
#         on_delete=models.SET_DEFAULT,
#         default=get_default_offers,
#         related_name='subscriptions',
#         verbose_name=_("Offer")
#     )
#     start_date = models.DateField(verbose_name=_("Start Date"))
#     end_date = models.DateField(verbose_name=_("End Date"))
#     is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
#     is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
#     free_days = models.IntegerField(default=0, verbose_name=_("Free Days"))
#     descount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Discount"))
#     remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Remaining Balance"))

#     def save(self, *args, **kwargs):
#         self.is_active = not self.is_expired()
#         if self._state.adding and not self.remaining_balance:
#             self.remaining_balance = self.offer.price
#         super().save(*args, **kwargs)

#     def is_expired(self):
#         return self.end_date < timezone.now().date()

#     def __str__(self):
#         return f"{self.member.name} - {self.start_date} to {self.end_date}"

class Payment(models.Model):
    # PAYMENT_CHOICES = [
    #     ('VISA', 'Visa'),
    #     ('CASH', 'Cash'),
    # ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    #paymen_type = models.CharField(max_length=4, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"{self.subscription.member.name} - {self.amount_paid}"

# class Payment(models.Model):
#     # PAYMENT_CHOICES = [
#     #     ('VISA', 'Visa'),
#     #     ('CASH', 'Cash'),
#     # ]
#     member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Member"))
#     subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name=_("Subscription"))
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount Paid"))
#     payment_date = models.DateField(auto_now_add=True, verbose_name=_("Payment Date"))
#     #paymen_type = models.CharField(max_length=4, choices=PAYMENT_CHOICES)

#     def __str__(self):
#         return f"{self.subscription.member.name} - {self.amount_paid}"





#لتسجيل الاشعارات 
class Notification(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} - {self.message[:50]}"

def Notifications():
    return Notification.objects.all().order_by('-date_sent')

# # #  (Subscription) يمكن أن يكون له عدة اشتراكات ، (Member)العضو 

# # # الإشعارات (Notification) ترسل إلى الأعضاء (Member).






def create_classroom( name, description, dayofweek, starttime, endtime ):
    new_class = Classroom.objects.create(name=name,description=description,day_of_week=dayofweek,start_time=starttime,end_time=endtime)
    return new_class
    
def get_all_classrooms():
    return Classroom.objects.all()


def get_classroomes_set(id):
    class_room = Classroom.objects.get(id=id)
    members = class_room.members.all()
    return members
#you can return all the classroom members by member_set :
# DONT usr a related_name in the member class
# def get_classroomes_set(id):
#     class_room = Classroom.objects.get(id=id)
#     members = class_room.member_set.all()
#     return members

def create_offer(offer_name, description, price, duration_months):
    new_offer = Offer.objects.create(offer_name=offer_name, description=description, price=price, duration_months=duration_months)
    return new_offer

def get_all_offers():
    return Offer.objects.all()

def create_member(name, phone, email, classID):
    class_id = Classroom.objects.get(id=classID)
    new_member = Member.objects.create(name=name, phone_number=phone, email=email, class_name=class_id)
    return new_member

def get_all_members():
    members = Member.objects.all()
    return members

def get_classroom(id):
    return Classroom.objects.get(id=id)

def get_classroom_members(id):
    the_class = Classroom.objects.get(id=id)
    return the_class.members.all().order_by('-created_at')

def get_member_id(id):
    return Member.objects.get(id=id)

def create_subscription(member_id, offer_id , start_date, end_date, free_days, descount):
    
    offer = Offer.objects.get(id=offer_id)
    
    new_subscription = Subscription.objects.create(member=member_id, offer=offer, start_date=start_date, end_date=end_date, free_days=free_days, descount=descount)
    print(f"Subscription is created")
    return new_subscription

################################################### Here you can use Django Signals 
def update_member_balance(member_id):
    try:
        # Get the member
        member = Member.objects.get(id=member_id)
        # Get the member's latest subscription (Handle case if no subscription exists)
        subscription = member.subscriptions.order_by('-id').first() #start_date
        if not subscription:
            print(f"No subscription found for member {member_id}")
            return None  # Or return an appropriate response
        
        # Get the offer price from the subscription
        offer_price = subscription.offer.price
        #Handling Discounts and Free Days
        final_price = offer_price - subscription.descount

        # Update the member's balance 
        member.balance += max(final_price, 0)  # Ensure balance doesn't go negative
        member.save()

        print(f"Member {member_id} now has a balance of {member.balance}")
        return member  # Returning the updated member object if needed
    except Member.DoesNotExist:
        print(f"Member with ID {member_id} does not exist.")
        return None
################################################## Here you can use Django Signals



#get the class room from member
def get_classroom_id_from_member(member_id):
    member = Member.objects.get(id=member_id)
    return member.class_name.id if member.class_name else None

def get_subscription_by_member(member_id):
    member = Member.objects.get(id=member_id)
    return member.subscriptions.all()


def get_expired_subscriptions():
    today = timezone.now().date()
    Subscription.objects.filter(end_date__lt=today, is_active=True).update(is_active=False)
    # return Subscription.objects.filter(end_date__lte=today) ##مش مدفوع و منتهي
    # الأعضاء الذين انتهى آخر اشتراك لهم
    # return Member.objects.filter(subscriptions__end_date__lt=today).distinct()
    # Get the last subscription per member
    last_subscription = Subscription.objects.filter(member=OuterRef('pk')).order_by('-id').values('is_active')[:1]
    # Filter members where the last subscription is inactive
    return Member.objects.annotate(last_subscription_status=Subquery(last_subscription)).filter(last_subscription_status=False)
    # return Member.objects.filter(subscriptions__is_active=False ).distinct() 
