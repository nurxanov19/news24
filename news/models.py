from django_ckeditor_5.fields import CKEditor5Field
from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300)
    description = CKEditor5Field(config_name='default')
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='news_image', default='news_image/default.jpeg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.category})"


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.message}"


