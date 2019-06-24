
from django.db import models

# Create your models here.
from django.utils import timezone

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


class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)  # ip 주소
    post = models.ForeignKey(Board, to_field='id', default=None, null=True, on_delete=models.CASCADE)  # 게시글
    date = models.DateField(default=timezone.now(), null=True, blank=True)  # 조회수가 올라갔던 날짜
