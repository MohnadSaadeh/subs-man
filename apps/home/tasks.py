# # apps/home/utils.py أو tasks.py
# from django.utils import timezone
# from .models import Subscription, Notification

# def check_expired_subscriptions_and_notify():
#     today = timezone.now().date()
#     expired_subs = Subscription.objects.filter(end_date__lt=today, is_active=True)

#     for sub in expired_subs:
#         member = sub.member

#         # تأكد ألا يكون هناك تنبيه مكرر
#         already_notified = Notification.objects.filter(
#             member=member,
#             message__icontains="انتهى اشتراكك",
#             date_sent__date=sub.end_date
#         ).exists()

#         if not already_notified:
#             # تحديث حالة الاشتراك
#             sub.is_active = False
#             sub.save()

#             # إنشاء التنبيه
#             Notification.objects.create(
#                 member=member,
#                 message=f"انتهى اشتراكك بتاريخ {sub.end_date}. يرجى التجديد."
#             )
