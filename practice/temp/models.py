from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=50,null=True)
    email=models.EmailField(unique=True,null=False)
    bio=models.TextField(null=True)
    avatar=models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]



class Topic(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Rooom(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description=models.CharField(max_length=100,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    participants=models.ManyToManyField(User, related_name='participants' , blank=True)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.name

class Messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Rooom,on_delete=models.CASCADE)
    body=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.body[0:50]
#