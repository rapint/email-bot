from django.db import models

class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    app_password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
