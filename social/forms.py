from django import forms
from .models import About, Message, Profile, Notification,Comment,Mention, Post
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignInForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))

class CustomUserCreationForm(UserCreationForm):
    phone_number=forms.CharField(max_length=30)

class Meta(UserCreationForm.Meta):
    model=User
    fields=('username','email','password1','password2','firstname')
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['went_to','work_at','live_in','from_where',
                  ]
        widgets = {
             'went_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'went_to',}),
             'work_at': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'work_at'}),
             'live_in': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'live_in'}),
             'from_where': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'from_where'}),   
        }


class PostForm(forms.ModelForm):
    mentioned_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={'class':'form-group'}),  
            'image': forms.FileInput(),  
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment-form-container', 'id': 'content', 'rows': 4, 'placeholder': 'Type your comment here...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'message_content']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = []  
    def mark_as_read(self):
        notification_instance = self.instance  
        notification_instance.delete()


class MentionForm(forms.ModelForm):
    class Meta:
        model = Mention
        fields = ['mentioned_user', 'post']



