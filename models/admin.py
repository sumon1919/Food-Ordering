from django.contrib import admin
from .models import *
from django.db.models import Sum

admin.site.register(Product)
admin.site.register(StudentID)
class studentAdmin(admin.ModelAdmin):
    list_display = ['student_name','student_email']
admin.site.register(Student,studentAdmin)
admin.site.register(Department)
admin.site.register(Subject)

class SubjectMarkAdmin(admin.ModelAdmin):
    list_display = ['student','subject','marks']
admin.site.register(SubjectMarks,SubjectMarkAdmin)

class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student','student_ranks','total_marks','data_of_report_card_generation']
    ordering = ['student_ranks']
    def total_marks(self,obj):
        subject_marks = SubjectMarks.objects.filter(student = obj.student)
        marks = (subject_marks.aggregate(marks = Sum('marks')))
        print()
        return marks['marks']
admin.site.register(ReportCard, ReportCardAdmin)