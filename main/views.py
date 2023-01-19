import json
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from main.forms import ContactForm, MainParticipantForm, MemberForm, MemberdetailsviewprofileForm, MentordetailsviewprofileForm, NewUserForm, MentordetailsForm,ShowMentordetailsForm, AddMemberDetailsForm, UpdateMainParticipantForm, UpdateMemberdetailsForm, UpdateMentorForm, ViewmainParticipantForm
from django.contrib.auth.models import User

from main.models import Book, Institution

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import MainParticipant, Memberdetails, Problem, Institution,Mentordetails, Solution_details
# Create your views here.

# frontend
# landing site
def index(request):
  return render(request,"main/landing/index.html")
def faq(request):
  return render(request,"main/landing/faq.html")
def plbmstmt(request):
  return render(request,"main/landing/problemstatements.html")
def guidelines(request):
  return render(request,"main/landing/guidelines.html")

def homepage(request):
    books = Book.objects.all()
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        mainParticipantDetails = MainParticipant.objects.get(user_id=request.user)
    return render(request=request, template_name='main/home.html', context={"books": page_obj,'user':mainParticipantDetails})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Inquiry'
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@icfoss.org',
                          ['admin@icfoss.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent.")
            return redirect("main:homepage")
    form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successfull")
            return redirect("main:registration")
        messages.error(
            request, f"Unsuccessful Registration, {form.error_messages}")
    if request.user.is_authenticated:
        return redirect('main:homepage')
    form = NewUserForm()
    return render(request, 'main/register.html', {'register_form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    login(request, user)
                    main_participant = MainParticipant.objects.get(user_id = user)
                except:
                    return redirect('main:registration')
                
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
        return render(request=request, template_name="main/login.html", context={"login_form": form})
    else:
        if request.user.is_authenticated:
            return redirect('main:homepage')
        form = AuthenticationForm()
        return render(request=request, template_name="main/login.html", context={"login_form": form})
   
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:index")


def registration_request(request):
    if request.method == "POST":
     form = MainParticipantForm(request.POST,request.FILES)
     if form.is_valid():
        mainparicipant = form.save(commit=False)
        mainparicipant.user_id = request.user
        mainparicipant.status = 'U'
        mainparicipant.save()
        from django.http import JsonResponse
        return redirect('main:problem')
     institution = Institution.objects.all()
     form = {
        'institution': institution
    }
     return redirect("main:registration")
    
    form = NewUserForm()
    return render(request, 'main/registration.html', {'register_form': form})

def proposal_submission(request):
    if request.method == 'POST':
        print("post", request.POST, "files", request.FILES)

        return HttpResponse("Submitted")

from django.http import JsonResponse

def problem_description(request):
    if request.method == 'POST':
        print("problem_id", request.POST['problem_id'])
        problem = Problem.objects.get(problem_id = request.POST['problem_id'])
        print("problem_description", problem_description)
        return JsonResponse({"description": problem.description})

def problem(request):
    if request.method == 'POST':

        usersignupdetails = {
                "solution_upload" : request.FILES['solution_upload']
            }
        print(request.POST.dict())
        plbm = Problem.objects.get(problem_id = request.POST.dict()['institution_name'])
        instance = Solution_details.objects.create(user_id =request.user,problem_id =plbm,**usersignupdetails)
        instance.save()
        return redirect('main:homepage')
    else:
        problems = Problem.objects.all()
        return render(request,'main/problem.html', {'problems':problems})


from django.views import View

class MentorDetails(View):
    form_class = ShowMentordetailsForm
    template_name = "main/viewmentorprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            memberdetails = Memberdetails.objects.filter(user_id=request.user)
            print(len(list(memberdetails)))
            # check member details
            return render(request, self.template_name, {"form": form, "memberdetails": [member for member in memberdetails.values()]})
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form})
        
    def post(self, request, *args, **kwargs):
        pass

class AddMember(View):
    form_class = AddMemberDetailsForm
    template_name = "main/members.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        
        return render(request, self.template_name, {"form": form})
        
    def post(self, request, *args, **kwargs):  
        if request.method == "POST":
            form = MemberForm(request.POST,request.FILES)
            # try:
            #     members = Memberdetails.objects.get(user_id = request.user)
            # except: 
            #     members = {}
            print(request.POST)
            if form.is_valid():
                print("valid")
                mentordetails = form.save(commit=False)
                mentordetails.user_id = request.user
                md=Mentordetails.objects.filter(user_id=request.user)
                
                mentordetails.save()
                return redirect('main:homepage')
                # return render(request, 'main/members.html')
                # context = {"form": form, "members":members}
                # return render(request, 'main/members.html', context)  

            else:
                context = {"form": form}
                return render(request, 'main/members.html', context)  
        
        else:
            
            return render(request, 'main/members.html')  
                # form = self.form_class(request.POST)
                # if form.is_valid():
                #     form.save()
                #     redirect('main:member')
                # return render(request, self.template_name, {"form": form})
        
    
def mentordetails(request):
 if request.method == "POST":
    form = MentordetailsForm(request.POST)

    if form.is_valid():
         mentorDetails = form.save(commit=False)
         mentorDetails.user_id =request.user
        #  md=Memberdetails.objects.filter(user_id=request.user)
        #  d=len(list(md))
        #  if d>=1:
        #   return redirect("main:homepage")
         mentorDetails.save()
         return redirect('main:homepage')
    else:
        redirect('main:mentordetails')

    return render(request, 'main/mentordetails.html')
 else:
    return render(request, 'main/mentordetails.html')

from django.contrib.auth.decorators import login_required
# @login_required(login_url='/login/')
def memberdetails(request):
 if request.method == "POST":
    form = MemberForm(request.POST,request.FILES)
    try:
        members = Memberdetails.objects.get(user_id = request.user)
    except: 
        members = {}
    if form.is_valid():
        memberDetails = form.save(commit=False)
        memberDetails.user_id = request.user
        memberDetails.save()
        

        context = {"form": form, "members":members}
        return render(request, 'main/members.html', context)  

    else:
        context = {"form": form}
        return render(request, 'main/members.html', context)  
   
 else:
    return render(request, 'main/members.html')


# profile view- Home Page



class ViewMemberProfile(View):
    form_class = MemberdetailsviewprofileForm
    template_name = "main/viewmemberprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            memberdetails = Memberdetails.objects.filter(user_id=request.user)
            print(len(list(memberdetails)))
          
            return render(request, self.template_name, {"form": form, "memberdetails": [member for member in memberdetails.values()], 'length':len(list(memberdetails))})
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form, 'length':0})

class ViewMentorProfile(View):
    form_class = MentordetailsviewprofileForm
    template_name = "main/viewmentorprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            menterprofile = Mentordetails.objects.get(user_id=request.user)
            print(menterprofile)
            return render(request, self.template_name, {"form": form, "mentordetails": menterprofile, 'length':1})
        
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form, 'length':0})
    
    
class ViewUserProfile(View):
    form_class = ViewmainParticipantForm
    template_name = "main/viewuserprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            mainparticipantdetails = MainParticipant.objects.get(user_id=request.user)
            print(mainparticipantdetails)
            
            return render(request, self.template_name, {"participant": mainparticipantdetails})
        except MainParticipant.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form})   
    
class UpdateMentorProfile(View):
    form_class = UpdateMentorForm
    template_name = "main/viewmentorprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            menterprofile = Mentordetails.objects.get(user_id=request.user)
             
            
            return render(request, self.template_name, {"form": form, "mentordetails": menterprofile})
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form}) 
    
class UpdateUserProfile(View):
    form_class = UpdateMainParticipantForm
    template_name = "main/viewuserprofile.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            mainparticipantdetails = MainParticipant.objects.get(user_id=request.user,instance=form)
            
            
            return render(request, self.template_name, {"participant": mainparticipantdetails})
        except MainParticipant.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form}) 
    
    
class UpdateMemberProfile(View):
    form_class = UpdateMemberdetailsForm
    template_name = "main/show-member-details.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            memberdetails = Memberdetails.objects.filter(user_id=request.user)
            
          
            return render(request, self.template_name, {"form": form, "memberdetails": memberdetails})
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form})