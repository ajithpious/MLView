from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(max_length=20,primary_key=True)
    password=models.CharField(max_length=20)
    class Meta:
        db_table="user"


