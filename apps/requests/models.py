from django.db import models

class Request(models.Model):
    date = models.DateTimeField(auto_now=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    server_protocol = models.CharField(max_length=12)
    ip_addr = models.CharField(max_length=100)
    viewed = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
