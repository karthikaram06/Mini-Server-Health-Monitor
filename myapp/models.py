from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Server(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    server_name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=100)
    cpu_usage = models.IntegerField()
    ram_usage = models.IntegerField()
    disk_usage = models.IntegerField()
    status = models.CharField(max_length=20)
    overall_health = models.CharField(max_length=20, default="Unknown")

    def __str__(self):
        return self.server_name
    