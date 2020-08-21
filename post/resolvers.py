from post.models import Post

from graphene_django.views import GraphQLError

from graphtest.errors import *

def resolve_create_post(user_id, post_input):
    if str(user_id) == post_input.user_id:
        post_instance = Post(
            title = post_input.title,
            content = post_input.content,
            user_id = post_input.user_id
        )
        post_instance.save()
        return post_instance
    has_permissions()

def resolve_update_post(user_id, post_input, kwargs):
    post_instance = Post.objects.get(pk=kwargs.get('id'))

    post_user_id = post_instance.user.id

    if str(user_id) == str(post_user_id):
        if post_input.title:
            post_instance.title = post_input.title
        if post_input.content:
            post_instance.content = post_input.content

        post_instance.save()
        return post_instance
    has_permissions()

def resolve_delete_post(user, kwargs):
    post_instance = Post.objects.get(pk=kwargs.get('id'))

    post_user_id = str(post_instance.user.id)
    user_logged = str(user.id)

    if post_user_id == user_logged:
        post_instance.delete()

        return True
    has_permissions()

