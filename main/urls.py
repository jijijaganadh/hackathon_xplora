from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'main'

urlpatterns = [
    # landing urls
    path('',views.index,name="index"),
    path('faq/',views.faq,name="faq"),
    path('problemstatements/',views.plbmstmt,name="plbmstmt"),
    path('guidelines/',views.guidelines,name="guidelines"),
    path('about/',views.about,name="about"),

    # login urls
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    # reviewer urls
    path("reviewerhome/", views.Reviewerhome, name='reviewerhome'),
    path("reviewer-userview/<int:id>", views.Revieweruserview.as_view(), name='userview'),

    path("home/", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact"),
    path("logout/", views.logout_request, name="logout"),
    path("registration/", views.registration_request, name="registration"),
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
    path("deletementor/", views.DeleteMentor.as_view(), name="deletementor"),
    path("delete-member/<int:id>", views.DeleteMember.as_view(), name="deletemember"),
    path("viewproblem/", views.ViewProblemdetails.as_view(), name='viewproblem'),
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),

    
     # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='main/password_reset_form.html',
             subject_template_name='main/password_reset_subject.txt',
             email_template_name='main/password_reset_email.html',
             success_url='/password-reset_done'
         ),
         name='password_reset'),
    path('password-reset_done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='main/password_reset_done.html'
              
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/password_reset_confirm.html',
             success_url='/password-reset-complete'

         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

