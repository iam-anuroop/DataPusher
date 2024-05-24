from django.db import models
import uuid
import secrets


class Account(models.Model):
    emailid = models.EmailField(max_length=255,unique=True)
    accountid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=50,editable=False)
    website = models.URLField(null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = secrets.token_urlsafe(20)
        super().save(*args, **kwargs)


class Destination(models.Model):
    HTTP_METHODS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    ]
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10,choices=HTTP_METHODS)
    headers = models.JSONField()

