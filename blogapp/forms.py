from django import forms
from .models import Post,Comment

# class PostForm(forms.ModelForm):
    
#     class Meta:
#         model = Post
#         fields = ("",)
#         widgets = {
#             'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
#         }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','id':"fe-name" ,'name':"fe-name" ,'required':"required",'placeholder':"jhon Doe"}),         
            'email':forms.TextInput(attrs={'class':'form-control','id':"fe-email" ,'email':"fe-email", 'required':"required",'placeholder':"Your Email"}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'body': 'Body',
        }

class ShareForm(forms.Form):
         name = forms.CharField(widget=forms.TextInput(attrs={'class':'name','id':"fe-name" ,'name':"fe-name" ,'required':"required",'placeholder':"jhon Doe"}),label="Your Name")         
         email=forms.EmailField(widget=forms.TextInput(attrs={'class':'email','id':"fe-email" ,'email':"fe-email", 'required':"required",'placeholder':"Your Email"}),label="Your Email")
         to=forms.EmailField(widget=forms.TextInput(attrs={'class':'email','id':"fe-email" ,'email':"fe-email", 'required':"required",'placeholder':"To Email"}),label="To Email")
         comment = forms.CharField(widget=forms.Textarea(attrs={'class':'message'}), label="Comment")


# class Form(forms.Form):
class SubscribeForm(forms.Form):
         email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form_newsletter','id':"subEmail" , 'required':"required",'placeholder':"Your Email"}))

# class SearchForm(forms.Form):
#     query=forms.CharField()
