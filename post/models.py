from django.db import models
import uuid
import os
from datetime import datetime

from users.models import User

def upload_to(instance, filename):
  filetype = filename.split('.')[-1]
  return os.path.join('../tmp/%s/imgs/posts' % instance.user.id,
                        str(hash(datetime.now())) + '.' + filename)

# Create your models here.
class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=100, null=False)
  content = models.TextField()
  visualize = models.BooleanField(default=False)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.title

class PostImage(models.Model):
  post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
  image = models.ImageField(upload_to=upload_to)
  def __str__(self):
    return self.post.title
