from wsgiref.validate import validator
from django import forms
# from click import Choice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MainParticipant, Memberdetails,Mentordetails, Solution_details

# from .models import Solution


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    
class MainParticipantForm(forms.ModelForm):
    class Meta:
        model = MainParticipant
        fields = '__all__'
        
class MentordetailsForm(forms.ModelForm):
    class Meta:
        model = Mentordetails
        fields = ['name',"phoneno","email",'institution_name','designation','upload_photo']
    
class ShowMentordetailsForm(forms.ModelForm):
    class Meta:
        model = Mentordetails
        fields = ['name',"phoneno","email",'institution_name','designation','upload_photo']
        
class ViewproblemdetailsForm(forms.ModelForm):
    class Meta:
        model= Solution_details
        fields = ['solution_upload']  
        
        
class MainParticipantForm(forms.ModelForm):
    class Meta:
        model = MainParticipant
        fields = ['teamleadname','college_id',"phone",'institution_name','institution_address','upload_photo', 'usertype']


class NewUserForm(UserCreationForm):
     email = forms.EmailField(required=True)

     class Meta:
         model = User
         fields = ("username", "email",
                   "password1", "password2",)
#     class Meta:
#         model = MainParticipant
#         # fields = ("teamleadname", "phoneno",
#         #           "Institution", "Institution_id",)
        
#     class Meta:
#         model = Solution
        # fields = ("problem_statment_type", "file_upload")

     def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

def phone_number_validator(value):
    
    if len(value) < 9:
        raise ValueError('error')


class MemberForm(forms.ModelForm):
    class Meta:
        model= Memberdetails
        fields=('name','email','phoneno','institution_name','institution_id','upload_photo')  
    
    def clean(self):
        super().clean()   
        data = self.cleaned_data
        phoneno = data['phoneno']
        if phoneno and len(phoneno) < 8:
            import re
            phone_regex = '^\\+?[1-9][0-9]{9}$'
            if not re.match(phone_regex, phoneno):
                raise forms.ValidationError({"phoneno": "Phone number is invalid"})  
        return data
    
        
        
class AddMemberDetailsForm(forms.ModelForm):
    
    class Meta:
        model = Memberdetails
        fields = '__all__'
        
#    home page     

class MemberdetailsviewprofileForm(forms.ModelForm):
    class Meta:
        model= Memberdetails
        fields=('name','email','phoneno','institution_name','institution_id','upload_photo')  
    
class ViewmainParticipantForm(forms.ModelForm):
    class Meta:
        model = MainParticipant
        fields = ['teamleadname','college_id',"phone",'institution_name','institution_address']

class MentordetailsviewprofileForm(forms.ModelForm):
    class Meta:
        model = Mentordetails
        fields = ['name',"phoneno","email",'institution_name','designation','upload_photo']
    
class UpdateMentorForm(forms.ModelForm):
    class Meta:
        model = Mentordetails
        fields = ['name',"phoneno","email",'institution_name','designation']

class UpdateMainParticipantForm(forms.ModelForm):
    class Meta:
        model = MainParticipant
        fields = ['teamleadname',"phone",'institution_name','institution_address']

    def clean(self):
        return super().clean()

class UpdateMemberdetailsForm(forms.ModelForm):
    class Meta:
        model= Memberdetails
        fields=('name','email','phoneno','institution_name')  
    