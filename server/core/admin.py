from django import forms
from django.shortcuts import render
from django.urls import path
from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget
from django.contrib.auth.admin import UserAdmin

from .models import Question, User_Event, User_Question, Event, User_Result, User
# Register your models here.
class CsvImp(forms.Form):
    csv_upload=forms.FileField()

class MyAdmin(admin.ModelAdmin):
    change_list_template = 'change_list.html'
    def get_urls(self):
        urls=super().get_urls()
        new_urls=[path('upload-csv/',self.upload_csv)]
        return new_urls+urls
    def upload_csv(self,request):
        if request.method=='POST':
            csv_file=request.FILES["csv_upload"]
            file_data=csv_file.read().decode("utf-8")
            csv_data=file_data.split('\n')
            for x in range(1,len(csv_data)-2):
                fields=csv_data[x].split(",")
                created=Question.objects.update_or_create(
                    # id=fields[0],
                    statement=fields[0],
                    options=[fields[1],fields[2],fields[3],fields[4]],
                    correct_option=fields[5],
                )
        form=CsvImp()
        data={"form":form}
        return render(request,'csv_upload.html',data)
    
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields',
            {
                'fields': (
                    'current_user_event',
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)

admin.site.register(Question,MyAdmin)

admin.site.register(User_Event)
admin.site.register(User_Question)
admin.site.register(Event)
admin.site.register(User_Result)