from django.db import models
from django.contrib.auth.models import User



    
class Post(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    content = models.ImageField(upload_to='static/image/')
    publication_date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username