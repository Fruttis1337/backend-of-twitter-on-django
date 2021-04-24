from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=12)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Tweets(models.Model):
    text = models.TextField()
    photo = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.id}] [{self.author.username}] {self.text}'


class Follow(models.Model):
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follower')
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follows')
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'

