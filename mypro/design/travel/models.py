from django.db import models

# Create your models here.
class Place(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(default="")
    image=models.ImageField(upload_to='design/images',null=True,blank=True)
    def __str__(self):
        return self.name
class Team(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")
    image = models.ImageField(upload_to='team/images', null=True, blank=True)

    def __str__(self):
        return self.name

