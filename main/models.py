from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('category_tasks', args=[str(self.pk)])
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-important']

class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', default=1)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Заголовок", default="")
    description = models.TextField(null=True, blank=True, verbose_name=u"Описание", default="")
    complete =  models.BooleanField(default=False, verbose_name=u"Состояние")
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(verbose_name='Срок выполнения', blank=True, null=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)
    
    @property
    def is_overdue(self):
        return not self.is_completed and self.deadline < timezone.now()

    class Meta:
        ordering = ['-important', 'complete']

class AuthUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login
    
@receiver(pre_save, sender=Category)
def update_created_at(sender, instance, **kwargs):
    if instance.pk:
        instance.created_at = datetime.now()

@receiver(pre_save, sender=Task)
def update_created_at(sender, instance, **kwargs):
    if instance.pk:
        instance.created_at = datetime.now()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=50, unique=True)
    chat_id = models.CharField(max_length=50)
    notify_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})