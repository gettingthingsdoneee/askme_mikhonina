from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from app.models import Question, Answer, Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if len(username) > 12:
    #         raise forms.ValidationError('Too long')
    #     return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        return cleaned_data
    
    
class ProfileForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already taken')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError('Password is too short')
        return password


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            self.add_error(field='confirm_password', error="Passwords should match")

        return cleaned_data    

    def save(self, commit=True):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(username, email, password)

        profile = super().save(commit=False)
        profile.user = user
        profile.password = (self.cleaned_data.get('password'))

        if commit:
            profile.save()
        return profile
    

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    new_password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']
        labels = {
            'nickname': 'Display Name',
            'avatar': 'Profile Picture'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['nickname'].initial = self.user.profile.nickname

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (self.user and 
            self.user.username != username and 
            User.objects.filter(username=username).exists()):
            raise forms.ValidationError('Username is already taken')
        return username

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if password and len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            
        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            
            
            if self.cleaned_data['new_password']:
                self.user.set_password(self.cleaned_data['new_password'])
            
            if commit:
                self.user.save()
                profile.save()
                
        return profile
    
#  class ProfileForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
        
#         if password != confirm_password:
#             self.add_error(field='confirm_password', error="Passwords should match")

#         return cleaned_data    

#     def save(self):
#         user = super().save()
#         # profile
#         # user = User.objects.create_user(username, password)
#         user.set_password(self.cleaned_data.get('password'))
#         return user.save()   



# def LogoutForm(forms.Form)





    
class QuestionForm(forms.ModelForm):
    # name = forms.CharField(max_length=255)
    # text = forms.TextField(default='')
    # tag = forms.ManyToManyField('Tag')

    class Meta:
        model = Question
        fields = ['name', 'text', 'tag']

    

class AnswerForm(forms.ModelForm):
    # text = forms.TextField(default='')

    class Meta:
        model = Answer
        fields = ['text']

    




