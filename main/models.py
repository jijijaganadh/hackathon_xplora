import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Book(models.Model):
    book_title = models.CharField(max_length=150)
    publishing_year = models.IntegerField()
    author = models.CharField(max_length=100)
    plot = models.TextField()

    def __str__(self):
        return self.book_title
 



class Institution(models.Model):
   
    institution_name = models.CharField(max_length=500)
    class Meta:
          db_table="institution"
   
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user_id, filename)

class MainParticipant(models.Model):
    user_id= models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    teamleadname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=50)
    institution_address = models.CharField(max_length=500)
    # institution_id = models.ForeignKey(Institution, null=True, on_delete=models.CASCADE)
    college_id = models.FileField(upload_to=user_directory_path)
    status = models.CharField(max_length=1)
    # Status => U: underreview,A: accepted,R: rejected with remark
    remark= models.CharField(max_length=100,null=True)
    created_on=datetime.now().time()
    created_by=datetime.now().time()
    class Meta:
          db_table="main_participant"

class Mentordetails(models.Model):
    user_id= models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneno = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    class Meta:
          db_table="mentor_details"

          
class Problem(models.Model):
    problem_id = models.IntegerField(primary_key=True)
    problem_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    class Meta:
          db_table="problem_details"          

class Solution_details(models.Model):
     user_id= models.ForeignKey(User, null=True, on_delete=models.CASCADE)
     problem_id = models.ForeignKey('Problem', null=True, on_delete=models.CASCADE)
    #  description = models.CharField(max_length=50)
     solution_upload = models.FileField(upload_to=user_directory_path)

    
     class Meta:
          db_table="solution_details"

 
class Memberdetails(models.Model):
    user_id= models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneno = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=100)
    institution_id= models.FileField(upload_to=user_directory_path)

    class Meta:
          db_table="member_details"
 
