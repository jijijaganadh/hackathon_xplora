from django.contrib import admin

from .models import Book, MainParticipant, Memberdetails, Mentordetails, Problem, Solution_details

# Register your models here.

admin.site.register(Book)
admin.site.register(MainParticipant)
admin.site.register(Mentordetails)
admin.site.register(Problem)
admin.site.register(Solution_details)
admin.site.register(Memberdetails)
# admin.site.register(Solution_reviewer)





