from django import forms 
# to Extends the User Creation Form > the defult Form from Django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import CustomUser
# يوجد فورمم مخصص من الديجانغو لليوز
# انشاء كلة المرور وتغييرها وانشاء مشتخدم كلو جاهز
# وهو بيعطينا صفحة ديجانغو جاهزه
# بهاي الطرييقة ببنضيف على الفورم الاصليه
# في هذا المثال ضفنا ال ايمييل على الرجسستتريشن
# اذا ما بدك تضيف اي شي استخدمها جاهزه زي الوغن 
# ما الها يورل ولا فنكشن وخصصها بالصفحه زي صفحة الوغن
class RegisterForm(UserCreationForm):# adding a new form to the defult django user form > (UserCreationForm)
    email = forms.EmailField(required=True) # newly added

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]