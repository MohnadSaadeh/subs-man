# from django.db.signals import post_save
from django.db.models.signals import post_save  # ✅ CORRECT
from django.dispatch import receiver
from datetime import date
from .models import Payment , Member ,Subscription

@receiver(post_save , sender = Payment)
def update_member_balanc(sender , instance , created , **kwargs):
    if created:
        member = instance.member

        member.balance -= instance.amount_paid
        member.save()

        subscription = instance.subscription
        offer_price = subscription.offer.price

        # Subtract the payment amount from the remaining balance
        subscription.remaining_balance -= instance.amount_paid
        if subscription.remaining_balance <= 0:
            subscription.is_paid = True
            subscription.remaining_balance = 0  # Optionally reset remaining_balance when paid off
        
        subscription.save()

        """تحديث حالة العضو عند إجراء الدفع"""
        # إذا دفع، نتحقق من الاشتراكات الفعالة
        active_subscriptions = Subscription.objects.filter(member=member, end_date__gte=date.today())
        
        if active_subscriptions.exists() and member.balance == 0 :
            member.status = 'active'
        elif active_subscriptions.exists() and member.balance > 0 :
            member.status = 'overdue'
        elif not active_subscriptions.exists() and member.balance > 0:
            member.status = 'suspended' #مش مجدد و مديون
        else:
            member.status = 'expired'

        member.save()


@receiver(post_save, sender=Subscription)
def update_member_status_on_subscription (sender, instance, **kwargs):
    """تحديث الحالة عند إنشاء اشتراك جديد"""
    member = instance.member
    if instance.end_date >= date.today() and member.balance == 0:
        member.status = 'active'
    elif instance.end_date >= date.today() and member.balance > 0:
        member.status = 'overdue'
    elif instance.end_date < date.today() and member.balance > 0:
        member.status = 'suspended'
    else:
        member.status = 'expired'
    
    member.save()
    print(member.status)