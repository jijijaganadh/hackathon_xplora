from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    # landing urls
    path('',views.index,name="index"),
    path('faq/',views.faq,name="faq"),
    path('problemstatements/',views.plbmstmt,name="plbmstmt"),
    path('guidelines/',views.guidelines,name="guidelines"),

    # login urls
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),



    path("home/", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact"),
    path("logout/", views.logout_request, name="logout"),
    path("registration/", views.registration_request, name="registration"),
    # path("submission/", views.proposal_submission, name="submission"),
    # path("mentordetails/", views.mentor_details, name="mentordetails"),
    # path("participant/", views.participants, name="participant"),
    path("problem/", views.problem, name="problem"),
    path("mentor/", views.mentordetails, name="mentor"),
    path("member/", views.memberdetails, name="member"),
    path("problem_description", views.problem_description, name='problem_description'),


]

