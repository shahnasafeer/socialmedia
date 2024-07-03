from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, default='', blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"Profile for {self.name.username}"
class About(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    went_to=models.CharField(max_length=250, default='')
    work_at=models.CharField(max_length=250, default='')
    live_in=models.CharField(max_length=250, default='')
    from_where=models.CharField(max_length=250, default='')
    
    def __str__(self):
        return f"About {self.userid.username}" 

class Post(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    caption = models.TextField(null=False, default='')
    mentions = models.ManyToManyField(User, related_name='mentioned_in_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', through='Like')

   
    def __str__(self):
        return f"Post by {self.userid.username}"

    def create_notifications(self):
        followers = Follow.objects.filter(followed=self.userid).values_list('follower', flat=True)
        for follower_id in followers:
            follower = User.objects.get(pk=follower_id)
            Notification.objects.create(
                user=follower,
                message=f'{self.userid.username} added a new post.',
                post=self
            )
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def clean(self):
        existing_like = Like.objects.filter(user=self.user, post=self.post).exists()
        if existing_like:
            raise ValidationError('This user has already liked this post.')
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.user.username}'s post"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE,default="")
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE,default="")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.text[:20]}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20,default='')  
    message = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.type} - {self.message}'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')
class Mention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentioned_in')
    post = models.ForeignKey('Post', on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} mentioned {self.mentioned_user.username} in post {self.post.id}"




