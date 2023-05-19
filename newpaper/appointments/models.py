from django.db import models
from datetime import datetime
from news.models import Author, Post, Category
from django.contrib.auth.models import User
 
 
class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField()
    subscribers = models.ManyToManyField(Category, through = 'SubsCategory')
 
    def __str__(self):
        return f'{self.user}: {self.message}'

class SubsCategory(models.Model):
    users = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.users}: {self.category.categoryname}'




























































