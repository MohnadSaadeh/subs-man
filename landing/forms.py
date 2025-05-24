from django import forms
from tenants.models import ClientSignupRequest
class ClientSignupForm(forms.ModelForm):
    class Meta:
        model = ClientSignupRequest
        fields = ['name', 'email', 'phone', 'industry']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم النادي أو المؤسسة'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نوع النشاط'}),
        }