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
    path("member/", views.MentorDetails.as_view(), name="member"),
    path("add_member/", views.AddMember.as_view(), name="addmember" ),
    path("problem_description/", views.problem_description, name='problem_description'),
    path("userprofile/", views.ViewUserProfile.as_view(), name='userprofile'),
    path("memberprofile/", views.ViewMemberProfile.as_view(), name='memberprofile'),
    path("mentorprofile/", views.ViewMentorProfile.as_view(), name='mentorprofile'),
    path("updateuserprofile/", views.UpdateUserProfile.as_view(), name='userprofile'),
    path("updatememberprofile/<int:id>", views.UpdateMemberProfile.as_view(), name='memberprofile'),
    path("updatementorprofile/", views.UpdateMentorProfile.as_view(), name='updatementorprofile'),
    path("delete-mentor/", views.DeleteMentor.as_view(), name="deletementor"),
    path("delete-member/<int:id>", views.DeleteMember.as_view(), name="deletemember"),

]

