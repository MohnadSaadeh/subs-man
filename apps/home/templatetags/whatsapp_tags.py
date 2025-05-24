from django import template

register = template.Library()

@register.filter
def whatsapp_format(phone):
    phone = str(phone)
    if phone.startswith("0"):# حذف أول صفر وإضافة مفتاح الدولة 970
        phone = phone[1:]
        return f"970{phone}"
    else: return phone #ادخال الرقم مع المقدمه بدون +

