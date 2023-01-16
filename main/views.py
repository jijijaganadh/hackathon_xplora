import json
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from main.forms import ContactForm, MainParticipantForm, MemberForm, NewUserForm, mentordetailsForm
from django.contrib.auth.models import User

from main.models import Book, Institution

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import MainParticipant, Problem, Institution,Mentordetails, Solution_details
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
                    main_participant = MainParticipant.objects.get(user_id = user)
                except:
                    login(request, user)
                    return redirect('main:registration')
                
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
        return render(request=request, template_name="main/login.html", context={"login_form": form})
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="main/login.html", context={"login_form": form})
   
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


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
        return redirect('main:member')
    else:
        problems = Problem.objects.all()
        return render(request,'main/problem.html', {'problems':problems})


def mentordetails(request):
 if request.method == "POST":
    form = mentordetailsForm(request.POST)

    if form.is_valid():
        mentorDetails = form.save(commit=False)
        mentorDetails.user_id =request.user
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
    if form.is_valid():
        memberDetails = form.save(commit=False)
        memberDetails.user_id = request.user
        memberDetails.save()
        

        return redirect('main:mentor') 

    else:
        context = {"form": form}
        return render(request, 'main/members.html', context)  
   
 else:
    return render(request, 'main/members.html')

