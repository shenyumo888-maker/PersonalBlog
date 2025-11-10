from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    """
    用户注册表单
    """
    # 额外添加两个密码字段
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email') # 只让用户填写用户名和邮箱

    def clean_password2(self):
        """
        自定义验证方法，检查两次输入的密码是否一致
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次输入的密码不匹配。')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    """
    编辑用户基本信息（如邮箱）的表单
    """
    class Meta:
        model = User
        fields = ('email',)

class ProfileEditForm(forms.ModelForm):
    """
    编辑用户 Profile（简介和头像）的表单
    """
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')