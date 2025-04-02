from django.contrib.auth.models import User
from django.db import models



from news.models import News

#post = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='post_like')
    updated_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.content}"

    def number_of_likes(self):
        return self.like.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_picture/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.filter(user=self.user).exists():
            return  # Prevent duplicate profiles
        super().save(*args, **kwargs)
