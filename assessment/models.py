from django.db import models
import random, string
from mauth.models import User
# Create your models here.

class Categories(models.Model):
    category = models.CharField(max_length = 100)
    information = models.TextField()
    category_order = models.PositiveIntegerField(unique=True)
    photo = models.ImageField(upload_to= ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))+'/', blank=True)
    
    heading = models.CharField(max_length = 100, default='Default Heading') 

    def __str__(self):
        return f"{self.category}"


class Answers(models.Model):
    answer = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.answer}"

class Questions(models.Model):
    question = models.TextField()
    question_fk = models.ForeignKey(Categories, on_delete=models.CASCADE)
    question_order = models.PositiveIntegerField()
    task = models.TextField(default="This is a deafult task for this question.")
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('question_fk', 'question_order')

    def __str__(self):
        return f"{self.question}"


class Paragraphs(models.Model):
    paragraph = models.TextField()
    paragraph_fk = models.ForeignKey(Categories, on_delete=models.CASCADE)
    paragraph_order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('paragraph_fk', 'paragraph_order')

    def __str__(self):
        return f"{self.paragraph}"


class UserAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)  
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)  
    mdate = models.DateField(auto_now=True)

    class Meta:  
        unique_together = ('user', 'question')  
    def __str__(self):  
        return f'{self.user} {self.question} {self.answer}'  

class UserCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)  
    score  = models.PositiveIntegerField(default=0)
    class Meta:  
        unique_together = ('user', 'category', 'score')  
    def __str__(self):  
        return f'{self.user} {self.category} {self.score}'  


class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    radarChart = models.CharField(max_length = 100)
    barChart = models.CharField(max_length = 100)
    QuestionLock = models.BooleanField(default=False)
    Change = models.BooleanField(default=False)

    def __str__(self):  
        return f'{self.user} {self.QuestionLock}' 

class ResultPageParaghraphs(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE) 
    score  = models.PositiveIntegerField(default=0)
    paragraph = models.TextField()
    
    def __str__(self):  
        return f'{self.category} {self.score} {self.paragraph}' 






# python manage.py dumpdata auth --indent 2 > auth.json
# python manage.py loaddata fake_data.json

