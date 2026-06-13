from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from config.settings import AUTH_USER_MODEL
from materials.models import Course, Lesson


# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=35, verbose_name="Ф.И.О.", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        permissions = [("can_block_user", "Can block user")]


class Payment(models.Model):

    METHOD_CHOICES = [("cash", "Наличные"), ("transfer", "Перевод на счет")]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment')
    date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    status = models.CharField(max_length=30, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255,unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.amount}"

    class Meta:
        db_table = 'payment'
        verbose_name = "payment"
        verbose_name_plural = "payments"
