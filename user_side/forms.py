from django.core.files.images import get_image_dimensions
from django import forms
from .models import *

class ProfileImageForm(forms.ModelForm):
   class Meta:
       model = ProfileImage
       fields = '__all__'

#    def clean_picture(self):
#        picture = self.cleaned_data.get("image")
#        if not picture:
#            raise forms.ValidationError("No image!")
#        else:
#            w, h = get_image_dimensions(picture)
#            if w != 100:
#                raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 100px" % w)
#            if h != 200:
#                raise forms.ValidationError("The image is %i pixel high. It's supposed to be 200px" % h)
#        return picture
