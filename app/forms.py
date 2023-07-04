from django import forms
from .models import Post
from django.contrib.auth import(
    authenticate,
    get_user_model
   
)

User=get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'content']


class UserLoginForm(forms.Form):
    username=forms.CharField()
    password =forms.CharField(widget=forms.PasswordInput)

    def clean (self,*args,**kwargs):
        username =self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')
        if username and password:
            user =authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user dose not exist")
            if not user.check_password(password):
                raise forms.ValidationError("incorrect password")
            if not user.is_active:
                raise forms.ValidationError("The user is not actine")
        return super(UserLoginForm, self).clean(*args,**kwargs)
    


class UserRegisterForm(forms.ModelForm):
    email=forms.EmailField(label="Email address")
    email1=forms.EmailField(label="Confirm email")
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model =User
        fields=[
            'username',
            'email',
            'email1',
            
        ]
    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        email1=self.cleaned_data.get('email1')
        if email!=email1:
            raise forms.ValidationError("Emails must match")
        emails_qs=User.objects.filter(email=email)
        if emails_qs.exists():
            raise forms.ValidationError("alredy registerd")
        return super(UserRegisterForm,self).clean(*args,**kwargs)
