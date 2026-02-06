from django.db import models
# models.py
from django.contrib.auth.models import User

class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_accounts", null=True)
    email = models.EmailField()
    app_password = models.CharField(max_length=255)

    def __str__(self):
        return self.email