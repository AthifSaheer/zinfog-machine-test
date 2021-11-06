from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField()
    dob = models.DateField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
   