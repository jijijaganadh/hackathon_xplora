from email import message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
import json
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from main.forms import ContactForm, MainParticipantForm, MemberForm, MemberdetailsviewprofileForm, MentordetailsviewprofileForm, NewUserForm, MentordetailsForm, ShowMentordetailsForm, AddMemberDetailsForm, UpdateMainParticipantForm, UpdateMemberdetailsForm, UpdateMentorForm, ViewmainParticipantForm, ViewproblemdetailsForm
from django.contrib.auth.models import User
from main.models import Book, Institution
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import MainParticipant, Memberdetails, Problem, Institution, Mentordetails, Solution_details
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.urls import reverse



def index(request):
    return render(request, "main/landing/index.html")


def faq(request):
    return render(request, "main/landing/faq.html")


def plbmstmt(request):
    return render(request, "main/landing/problemstatements.html")


def guidelines(request):
    return render(request, "main/landing/guidelines.html")

def about(request):
    return render(request, "main/landing/about.html")
# reviewer dashboard
def reviewerhome(request):
    return render(request, "main/reviewer/reviewerhome.html")
def userview(request):
    return render(request, "main/reviewer/userview.html")




def homepage(request):
    books = Book.objects.all()
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        mainParticipantDetails = MainParticipant.objects.filter(
            user_id=request.user)
        solution_detals = Solution_details.objects.filter(user_id=request.user)
        if mainParticipantDetails.exists() and solution_detals.exists():
            problem_details = Problem.objects.filter(problem_id = solution_detals[0].problem_id.problem_id)
            return render(request=request, template_name='main/home.html', context={"books": page_obj, 'user': mainParticipantDetails[0], 'soln':solution_detals[0], 'problem_details': problem_details[0]},)
        elif not solution_detals.exists():
            return redirect('main:problem')
        else:
            return redirect('main:registration')


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

# sign up form
# @login_required(login_url='/login/')
def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        username=request.POST['username']
        try:
            if User.objects.filter(username=username):
                messages.error(request,"Username already exists, Please try again with different Username")
                return redirect('main:register')
            if form.is_valid():  
                user = form.save(commit=False)
                user.is_active = False
                user = form.save()
                send_activation_email(user, request)
                # login(request, user)
                messages.success(request, "Congratulations,Your Account has been created! we have sent you a confirmation mail please confirm your email to ativate your account")
                return redirect("main:register")
            messages.error(request, f"Unsuccessful Registration, Because {form.error_messages}")
        except Exception as e:
            messages.error(request,f"Entered Email already exists, Please try again with another Email")
    if request.user.is_authenticated:
        return redirect('main:homepage')
    
    form = NewUserForm()
    return render(request, 'main/register.html', {'register_form': form})

# login form
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
                    main_participant = MainParticipant.objects.get(
                        user_id=user)
                except:
                    return redirect('main:registration')
                return redirect("main:homepage")
        messages.error(request, f"Invalid username or password.")    
        return render(request=request, template_name="main/login.html", context={"login_form": form})
    else:
        if request.user.is_authenticated:
            return redirect('main:homepage')
        form = AuthenticationForm()
        return render(request=request, template_name="main/login.html", context={"login_form": form})

# logout form
def logout_request(request):
    logout(request)
    return redirect("main:index")

# collect main_participant profile details 
@login_required(login_url='/login/')
def registration_request(request):
    if request.method == "POST":
        form = MainParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            mainparicipant = form.save(commit=False)
            mainparicipant.user_id = request.user
            mainparicipant.status = 'U'
            mainparicipant.save()
            return redirect('main:problem')
        institution = Institution.objects.all()
        form = {
            'institution': institution
        }
        return redirect("main:registration")

    form = NewUserForm()
    current_user=request.user
    email=current_user.email
    context={'email':email}
    return render(request, 'main/registration.html', {'register_form': form,'participant':context})

@login_required(login_url='/login/')
def proposal_submission(request):
    if request.method == 'POST':
        print("post", request.POST, "files", request.FILES)

        return HttpResponse("Submitted")

# In html problem page -display each problem and their discription
@login_required(login_url='/login/')
def problem_description(request):
    if request.method == 'POST':
        print("problem_id", request.POST['problem_id'])
        problem = Problem.objects.get(problem_id=request.POST['problem_id'])
        print("problem_description", problem_description)
        return JsonResponse({"description": problem.description})

# save problems and their solutions in pdf format
@login_required(login_url='/login/')
def problem(request):
    if request.method == 'POST':
        print(request.FILES['solution_upload'].size <= 10000000)
        print(request.FILES['solution_upload'].size)
        usersignupdetails = {
            "solution_upload": 
                request.FILES['solution_upload']
        }

        if usersignupdetails['solution_upload'] and (usersignupdetails['solution_upload'].content_type == 'application/pdf') and usersignupdetails['solution_upload'].size <= 10000000: 
            
             # 10 MB file size limit
         print(request.POST.dict())
         plbm = Problem.objects.get(
            problem_id=request.POST.dict()['institution_name'])
         instance = Solution_details.objects.create(
            user_id=request.user, problem_id=plbm, **usersignupdetails)
         instance.save()
         return redirect('main:homepage')
        else:
            mainparticipantdetails = MainParticipant.objects.get(
                user_id=request.user)
            problemdetails = Problem.objects.filter(usertype=mainparticipantdetails.usertype).values()
            return render(request, 'main/problem.html', {'problems': problemdetails,'error':True})
    else:
        # find main Participant with user id
        #add user type to problemDetails model
        # mainparticipant.usertype
     try:
         mainparticipantdetails = MainParticipant.objects.get(
                user_id=request.user)
         usetype = mainparticipantdetails.usertype
        
        # print(usetype)
         problemdetails = Problem.objects.filter(usertype=usetype).values()
        # problemdetails = Problem.objects.all()
         print(problemdetails)
         return render(request, 'main/problem.html', {'problems': problemdetails})
     except Exception as e:
            return redirect("main:login")

# view mentor details
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


# add members details 
class AddMember(View):
    form_class = AddMemberDetailsForm
    template_name = "main/members.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = MemberForm(request.POST, request.FILES)
            # try:
            #     members = Memberdetails.objects.get(user_id = request.user)
            # except:
            #     members = {}
            print(request.POST)
            if form.is_valid():
                print("valid")
                mentordetails = form.save(commit=False)
                mentordetails.user_id = request.user
                md = Mentordetails.objects.filter(user_id=request.user)

                mentordetails.save()
                return redirect('main:memberprofile')
                # return render(request, 'main/members.html')
                # context = {"form": form, "members":members}
                # return render(request, 'main/members.html', context)

            else:
                context = {"form": form}
                return render(request, 'main/members.html', context)

        else:

            return render(request, 'main/members.html')
          
# save mentordetails
@login_required(login_url='/login/')
def mentordetails(request):
    if request.method == "POST":
        form = MentordetailsForm(request.POST,request.FILES)

        if form.is_valid():
            mentorDetails = form.save(commit=False)
            mentorDetails.user_id = request.user
            mentorDetails.save()
            return redirect('main:homepage')
        else:
            redirect('main:mentordetails')

        return render(request, 'main/mentordetails.html')
    else:
        return render(request, 'main/mentordetails.html')


# save memberdetail
@login_required(login_url='/login/')
def memberdetails(request):
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        try:
            members = Memberdetails.objects.get(user_id=request.user)
        except:
            members = {}
        if form.is_valid():
            memberDetails = form.save(commit=False)
            memberDetails.user_id = request.user
            memberDetails.save()

            context = {"form": form, "members": members}
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
            print(memberdetails)
            # print(memberdetails.institution.id)

            return render(request, self.template_name, {"form": form, "memberdetails": [member for member in memberdetails], 'length': len(list(memberdetails))})
        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form, 'length': 0})


class ViewMentorProfile(View):
    form_class = MentordetailsviewprofileForm
    template_name = "main/viewmentorprofile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            menterprofile = Mentordetails.objects.get(user_id=request.user)
            print(menterprofile)
            return render(request, self.template_name, {"form": form, "mentordetails": menterprofile, 'length': 1})

        except Mentordetails.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form, 'length': 0})


class ViewUserProfile(View):
    form_class = ViewmainParticipantForm
    template_name = "main/viewuserprofile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.user.id)
        try:
            mainparticipantdetails = MainParticipant.objects.get(
                user_id=request.user)
            # print(mainparticipantdetails.upload_photo.name.replace(""))
            # mainparticipantdetails.upload_photo = mainparticipantdetails.upload_photo.path
            return render(request, self.template_name, {"participant": mainparticipantdetails})
        except MainParticipant.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form})



class UpdateMentorProfile(View):
    form_class = UpdateMentorForm
    template_name = "main/updatementorprofile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        menterdetails = Mentordetails.objects.get(
            user_id=request.user)

        return render(request, self.template_name, {"form": form, "mentordetails": menterdetails})

    def post(self, request, *args, **kwargs):

        mentorprofile = Mentordetails.objects.get(user_id=request.user)
        form = self.form_class(request.POST, instance=mentorprofile)

        if form.is_valid():
            details = form.save()
            messages.success(request, "Updation Successfull")

            print(details)
        return render(request, self.template_name, {"mentordetails": details})


class DeleteMentor(View):
    def get(self, request):
        try:
            
            mentorprofiledetails = Mentordetails.objects.get(user_id=request.user)
            print(mentorprofiledetails)
            mentorprofiledetails.delete()
            return redirect("/mentorprofile/")
        except:
            pass

        return redirect("/mentorprofile/")
class DeleteMember(View):
    def get(self, request, id):
        try:
            memberprofile = Memberdetails.objects.filter(id=id)
            
            print(memberprofile)
            memberprofile.delete()
            return redirect("/memberprofile/")
        except:
            pass

        return redirect("/memberprofile/")


    
class UpdateUserProfile(View):
    form_class = UpdateMainParticipantForm
    template_name = "main/updateuserprofile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        mainparticipantdetails = MainParticipant.objects.get(
            user_id=request.user)

        return render(request, self.template_name, {"form": form, "participant": mainparticipantdetails})

    def post(self, request, *args, **kwargs):
        # print(request.user.id)
        participant = MainParticipant.objects.get(user_id=request.user)
        form = self.form_class(request.POST, instance=participant)

        if form.is_valid():
            data = form.save()
            print(data)
        return render(request, self.template_name, {"participant": data})

  
class UpdateMemberProfile(View):
    form_class = UpdateMemberdetailsForm
    template_name = "main/updatememberprofile.html"
    
    def get(self, request,id):
        form = self.form_class()
        memberdetails = Memberdetails.objects.get(
            user_id=request.user,id=id)
        return render(request, self.template_name, {"form": form, "member": memberdetails})
    
    def post(self, request,id):
        members = Memberdetails.objects.get(user_id=request.user,id=id)
        form = self.form_class(request.POST, instance=members)

        if form.is_valid():
            memberdetails = form.save()
            print(memberdetails)
        return render(request, self.template_name, {"member": memberdetails})

class ViewProblemdetails(View):
    form_class = ViewproblemdetailsForm
    template_name = "main/viewproblemdetails.html"

    def get(self, request):
        form = self.form_class()
        try:
            solutiondetails = Solution_details.objects.get(user_id=request.user)
            # print(solutiondetails.problem_id.problem_id)
            problemdetails = Problem.objects.get(problem_id=solutiondetails.problem_id.problem_id)
            print(solutiondetails)
            
            
            return render(request, self.template_name, {"form": form, "problemdetails": problemdetails,"solutiondetails":solutiondetails})

        except Solution_details.DoesNotExist:
            pass
        return render(request, self.template_name, {"form": form})



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# send activation email at the time of registration  
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    email.send()
    # if not settings.TESTING:
    #     EmailThread(email).start()
   
# activate user when clicking the link in email   
def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
        # user.is_active = True

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('main:login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})


# reviewer Home Page


