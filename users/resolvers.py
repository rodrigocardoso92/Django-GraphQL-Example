from users.models import User
from django.contrib.auth.hashers import make_password
import uuid

from graphtest.errors import *

def resolve_create_user(user_input):
    hashed_password = make_password(user_input.password)
    user_instance = User(
      username = user_input.username,
      email = user_input.email,
      bio = user_input.bio,
      password = hashed_password
    )
    user_instance.save()

    return user_instance

def resolve_update_user(logged_user_id, user_input, kwargs):
    user_id = kwargs.get('id')
    if logged_user_id == user_id:
        user_instance = User.objects.get(pk=user_id)
        if user_input.username:
          user_instance.username = user_input.username
        if user_input.email:
          user_instance.email = user_input.email
        if user_input.bio:
          user_instance.bio = user_input.bio
        if user_input.password:
          user_instance.password = make_password(user_input.password)
        user_instance.save()

        return user_instance
    has_permissions()

def resolve_delete_user(logged_user_id, kwargs):
    user_id = kwargs.get('id')
    if logged_user_id ==  user_id:
        user = User.objects.get(pk=user_id)
        user.delete()

        return True
    has_permissions()
