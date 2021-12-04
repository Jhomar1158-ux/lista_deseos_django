from django.db import models

# Create your models here.
class user(models.Model):
    name=models.CharField(default="Name*", max_length=255)
    username=models.CharField(default="Name*", max_length=200)
    password=models.CharField(max_length=255)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class items(models.Model):
    nameItem=models.CharField(max_length=255)
    uploader = models.ForeignKey(user, related_name = 'uploaded_item', on_delete = models.CASCADE)

# class (models.Model):
# 
#     pass

# class review(models.Model):
#     release = models.ForeignKey(user, related_name = 'release_date', on_delete = models.CASCADE)
