from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache

class Category(models.Model):
    categoryname = models.CharField(max_length = 64, unique = True)

    def __str__(self):
        return self.categoryname

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.IntegerField(default = 0)

    def update_rating(self):
        postrating = self.post_set.all().aggregate(allpost=Sum('ratingpost'))
        prat = 0
        prat += postrating.get('allpost')
        commentrate = self.user.comment_set.all().aggregate(allcomment=Sum('ratingcomment'))
        crat = 0
        crat += commentrate.get('allcomment')
        self.ratingAuthor = prat * 3 + crat
        self.save()
    
    def __str__(self):
        return f'{self.user}'

class Post(models.Model):
    POST = 'PO'
    NEWS = 'NE'
    TYPE_IN_PLACE = [
        (POST, 'post'),
        (NEWS, 'news'),
    ]
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    typepost = models.CharField(max_length = 2, choices = TYPE_IN_PLACE, default = POST)
    datepost = models.DateTimeField(auto_now_add = True)
    posts = models.ManyToManyField(Category, through = 'PostCategory')
    titlepost = models.CharField(max_length = 64, default = 'title')
    textpost = models.TextField()
    ratingpost = models.IntegerField(default = 0)

    def like(self):
        self.ratingpost += 1
        self.save()
    
    def dislike(self):
        self.ratingpost -= 1
        self.save()
    
    def preview(self):
        return self.textpost[0:50] + '...'
    
    def get_absolute_url(self):
        return f'http://127.0.0.1:8000/news/{self.id}'
    
    def get_category(self):
        category = self.posts.all()
        for i in category:
            category = i
        return category
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(self.pk) # затем удаляем его из кэша, чтобы сбросить его
    
    @property
    def on_rating(self):
        return self.ratingpost > 0

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.category.categoryname
    
    def get_category(self):
        return self.category.categoryname

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    textcomment = models.TextField()
    datecomment = models.DateTimeField(auto_now_add = True)
    ratingcomment = models.IntegerField(default = 0)

    def like(self):
        self.ratingcomment += 1
        self.save()

    def dislike(self):
        self.ratingcomment -= 1
        self.save()
    
    def __str__(self):
        try:
            return self.post.author.user.username
        except:
            return self.user.username








































