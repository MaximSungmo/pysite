from django.db import models

# Create your models here.
from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)