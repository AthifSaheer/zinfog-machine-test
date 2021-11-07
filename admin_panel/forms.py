from django import forms

from user_side.models import Student

class StudentForm(forms.ModelForm):
   class Meta:
       model = Student
       fields = ['mark']
    #    fields = '__all__'
