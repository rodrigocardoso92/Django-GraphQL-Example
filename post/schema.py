import graphene
from graphene_django import DjangoObjectType
import uuid

from post.models import Post
from users.models import User

class PostType(DjangoObjectType):
  class Meta:
    model = Post


class PostInput(graphene.InputObjectType):
  title = graphene.String()
  content = graphene.String()
  user_id = graphene.String()

class CreatePost(graphene.Mutation):
  class Arguments:
    post_input = PostInput(required=True)

  post = graphene.Field(PostType)

  @staticmethod
  def mutate(self, info, post_input=None):
    user_instance = User.objects.get(pk=post_input.user_id)
    post_instance = Post(
      title = post_input.title,
      content = post_input.content,
      user_id = post_input.user_id
    )

    post_instance.save()
    return CreatePost(post=post_instance)


class Query(graphene.ObjectType):
  posts = graphene.List(PostType)
  post_by_id = graphene.Field(PostType, id=graphene.String())

  def resolve_posts(self, info, **kwargs):
    return Post.objects.all()

  def resolve_post_by_id(self, info, **kwargs):
    return Post.objects.get(pk=kwargs.get('id'))


class Mutation(graphene.ObjectType):
  create_post = CreatePost.Field()