from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class countries(models.Model):
    country = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.country}"

class industries(models.Model):
    industry = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.industry}"
    
class myprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(countries, on_delete=models.CASCADE)
    industry = models.ForeignKey(industries, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} myprofile'

