from django import forms
from django.forms import widgets,ValidationError
from .models import *
from django.forms import ModelForm

# class LoginForm(forms.Form):
#     username = forms.CharField(label='username',max_length=100)
#     password = forms.CharField(label='password',max_length=100)
#
#     def clean_username(self):
#         if len(self.cleaned_data.get('username'))>5:
#             print(self.cleaned_data.get('password'))
#             return self.cleaned_data.get('username')
#         else:
#             raise ValidationError("用户名长度小于5")
#     def clean_password(self):
#         pass
#
#     def clean(self):
#         if  self.cleaned_data["password"] == self.cleaned_data['repeat_password']:
#             return  self.cleaned_data


class RegForm(forms.Form):

    username = forms.CharField(
        max_length=18,min_length=3,
        error_messages={"required":"用户名不能为空","min_length":"用户名少于3个字符","max_length":"用户名大于18个字符"},
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"username"}))

    password = forms.CharField(
        max_length=18,min_length=3,
        error_messages={"required": "密码不能为空", "min_length": "密码少于3个字符", "max_length": "用户名大于18个字符"},
        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"password"}))

    repeat_pwd = forms.CharField(
        error_messages={"required": "确认密码不能为空"},
        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"repeat_pwd"}))

    phone = forms.CharField(
        error_messages={"required": "手机号不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"手机号"}))

    def clean_username(self):
        ret = UserInfo.objects.filter(username=self.cleaned_data.get("username"))
        if not ret:
            return self.cleaned_data
        else:
            raise  ValidationError("用户名已注册")

    def clean_repeat_pwd(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")

    def clean_phone(self):
        if len(self.cleaned_data.get("phone")) == 11:
            return self.cleaned_data
        else:
            raise ValidationError("手机号格式不对")

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request


