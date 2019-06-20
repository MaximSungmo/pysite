from django.db import models


# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    content = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User({self.name}, {self.password}, {self.content}, {self.reg_date})'
