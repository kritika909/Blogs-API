from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_img', blank=True)
    bio = models.TextField(blank=True)
    accentcolor = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#[0-9A-Fa-f]{6}$',
            ),
        ],
        default='#75D8A2',
    )
    bgcolor = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#[0-9A-Fa-f]{6}$',
            ),
        ],
        default='#141414',
    )

    def __str__(self):
        return self.user.username
    
class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} follows {self.following}"
