from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Team(models.Model):
    name =  models.CharField(max_length=100,blank =True,null =True)
    def __str__(self):
        return self.name

class UserDetail(models.Model):
    user = models.ForeignKey( User, on_delete=models.DO_NOTHING,blank =True,null =True)
    designation = models.CharField(max_length=100,blank =True,null =True)
    profile_picture = models.ImageField(upload_to='picture/%Y/%m/%d',blank=True,null=True)
    team =  models.ManyToManyField(Team)
    
    def __str__(self):
        return self.user.username



