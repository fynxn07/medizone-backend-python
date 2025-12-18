from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
class CustomUser(AbstractUser):
    isBlock=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

