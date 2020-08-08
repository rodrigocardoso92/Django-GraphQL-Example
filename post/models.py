from django.db import models
import uuid

from users.models import User

# Create your models here.
class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=100)
  content = models.TextField()
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.title