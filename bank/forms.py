from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=45, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=45, widget=forms.PasswordInput(
        attrs={'class': 'form-control','placeholder': "Password"}))

class TransForm(forms.Form):
    dest_accnt = forms.IntegerField(label="目的账户", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "dest_accnt",'autofocus': ''}))
    amnt = forms.IntegerField(label="转账金额", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "amnt"}))

class DelForm(forms.Form):  # 用于销户
    del_accnt = forms.IntegerField(label="账号", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "del_accnt",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=45, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Password"}))