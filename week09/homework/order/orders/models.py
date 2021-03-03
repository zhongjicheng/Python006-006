from django.db import models

# Create your models here.
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class UserScore(models.Model):
    """
    用户积分
    """
    score = models.BigIntegerField(verbose_name='积分', default=0)
    username = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'user score'

    def __str__(self):
        return self.score

    @receiver(post_save, sender=User)
    def handler_user_create_content(sender, instance, created, **kwargs):
        if created:
            UserScore.objects.create(username=instance)

    @receiver(post_save, sender=User)
    def handler_user_save_content(sender, instance, created, **kwargs):
        instance.profile.save()


class Orders(models.Model):
    """
    订单类:
    一个订单的信息包含：产品名，产品的规格，数量，单价，总金额
    """
    __tablename__ = 'orders'
    product_id = models.IntegerField(verbose_name='产品id')
    product_name = models.CharField(max_length=30, verbose_name='产品名', default='')
    product_size = models.BigIntegerField(verbose_name='产品规格', default=1001)
    quantity = models.BigIntegerField(verbose_name='产品数量', default=0)
    price = models.BigIntegerField(verbose_name='产品单价', default=100)
    total_amount = models.BigIntegerField(verbose_name='总金额', default=0)
    is_cancel = models.BooleanField(verbose_name='取消订单', default=False)
    order_time = models.DateTimeField(auto_now_add=True)  # 下单时间
    create_order_time = models.DateTimeField(auto_now_add=True)  # 创建订单时间
