from django import forms
from django.shortcuts import render
from django.urls import path
from django.contrib import admin
from .models import Question
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
                fields=csv_data[x].split("|")
                try:
                    created=Question.objects.update_or_create(
                        # id=fields[0],
                        statement=fields[0],
                        options=[fields[1],fields[2],fields[3],fields[4]],
                        correct_option=fields[5],
                    )
                except:
                    pass
        form=CsvImp()
        data={"form":form}
        return render(request,'csv_upload.html',data)
admin.site.register(Question,MyAdmin)