from django.core.files.images import get_image_dimensions
from django import forms
from .models import *

class ProfileImageForm(forms.ModelForm):
   class Meta:
       model = ProfileImage
       fields = ['image']
    #    fields = '__all__'
