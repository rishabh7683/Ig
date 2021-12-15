from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ig_password=models.CharField(max_length=100,null=True)
    FullName=models.CharField(max_length=100,null=True)
    Mobile_Number=models.CharField(max_length=12,null=True)
    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return self.FullName


class Task(models.Model):
    owner=models.ForeignKey(Admin, null=True, blank=True, on_delete=models.SET_NULL)
    all_username=models.TextField(blank=True, null=True)
    task_name=models.CharField(max_length=256,blank=True,null=True)
    message=models.TextField(blank=True, null=True)
    action_time=models.DateTimeField()
    status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner.user)


class Chunk(models.Model):
    owner=models.ForeignKey(Admin, null=True, blank=True, on_delete=models.SET_NULL)
    task= models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    userji=models.TextField(blank=True, null=True)
    message=models.TextField(blank=True, null=True)
    execute=models.DateTimeField()
    user_sent=models.TextField(blank=True,null=True)
    user_notsent=models.TextField(blank=True,null=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner.user)
