import graphene
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLError
from django.db import connections
from graphql_jwt.decorators import login_required
import uuid

from graphtest.utils import test_db_connection

from post.models import Post
from users.models import User

from post.resolvers import *

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
  @login_required
  def mutate(self, info, post_input=None):
    if test_db_connection(connections):
      post_instance = resolve_create_post(post_input)
      return CreatePost(post=post_instance)
    else:
      raise GraphQLError('DB Server not connected!')

class UpdatePost(graphene.Mutation):
  class Arguments:
    id = graphene.UUID()
    post_input = PostInput(required=True)

  post = graphene.Field(PostType)

  @login_required
  def mutate(self, info, post_input=None, **kwargs):
    if test_db_connection(connections): 
      post_instance = resolve_update_post(post_input, kwargs)
      return UpdatePost(post=post_instance)
    else:
      raise GraphQLError('DB Server not connected!')

class DeletePost(graphene.Mutation):
  id = graphene.UUID()
  deleted = graphene.Boolean()
  class Arguments:
    id = graphene.UUID()
  
  post = graphene.Field(PostType)

  @login_required
  def mutate(self, info, **kwargs):
    if test_db_connection(connections):      
      deleted = resolve_delete_post(kwargs)
      return DeletePost(deleted=deleted)
      
    else:
      raise GraphQLError('DB Server not connected!')

class Query(graphene.ObjectType):
  posts = graphene.List(PostType)
  post_by_id = graphene.Field(PostType, id=graphene.String())

  def resolve_posts(self, info, **kwargs):
    if test_db_connection(connections):
      return Post.objects.all()
    raise GraphQLError('DB Server not connected!')

  def resolve_post_by_id(self, info, **kwargs):
    if test_db_connection(connections):
      return Post.objects.get(pk=kwargs.get('id'))
    raise GraphQLError('DB Server not connected!')


class Mutation(graphene.ObjectType):
  create_post = CreatePost.Field()
  delete_post = DeletePost.Field()
  update_post = UpdatePost.Field()