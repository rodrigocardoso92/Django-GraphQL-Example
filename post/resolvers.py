from post.models import Post



def resolve_create_post(post_input):
    post_instance = Post(
        title = post_input.title,
        content = post_input.content,
        user_id = post_input.user_id
      )
    post_instance.save()
    return post_instance

def resolve_update_post(post_input, kwargs):
    post_instance = Post.objects.get(pk=kwargs.get('id'))
    if post_input.title:
      post_instance.title = post_input.title
    if post_input.content:
      post_instance.content = post_input.content
    post_instance.save()
    return post_instance

def resolve_delete_post(kwargs):
    post = Post.objects.get(pk=kwargs.get('id'))
    post.delete()

    return True

