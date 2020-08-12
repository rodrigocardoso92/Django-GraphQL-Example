from users.models import User
from django.contrib.auth.hashers import make_password
import uuid

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

def resolve_update_user(user_input, kwargs):
    user_instance = User.objects.get(pk=kwargs.get('id'))
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

def resolve_delete_user(kwargs):
    user = User.objects.get(pk=kwargs.get('id'))
    user.delete()

    return True
