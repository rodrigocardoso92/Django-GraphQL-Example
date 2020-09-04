from users.models import User
from django.contrib.auth.hashers import make_password
import uuid

from graphtest.errors import *

def resolve_create_user(user_input):
    user_instance = User()

    for field, value in user_input.items():
        if field == 'password':
            user_instance.set_password(user_input.password)
        else:
            setattr(user_instance, field, value)

    user_instance.save()

    return user_instance

def resolve_update_user(logged_user_id, user_input, kwargs):
    user_id = kwargs.get('id')
    if logged_user_id == user_id:
        user_instance = User.objects.get(pk=user_id)
        for field, value in user_input.items():
            if field == 'password':
                user_instance.set_password(user_input.password)
            else:
                setattr(user_instance, field, value)
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
