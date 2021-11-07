from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    dob = models.DateField()
    age = models.PositiveIntegerField(default=0)
    mark = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if self.age == 0:
            dob_year = self.dob.split('-')
        else:
            dob_year = self.dob.strftime('%d')
        current_year = datetime.now().year
        age = int(current_year) - int(dob_year[0])
        self.age = age
        super().save(*args, **kwargs)

class ProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prf_img')
    updated_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.user.username)
