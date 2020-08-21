import graphene
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLError
from django.db import connections
from graphql_jwt.decorators import login_required
import uuid

from graphtest.utils import test_db_connection

from users.models import User

from users.resolvers import *

from graphtest.errors import *



class UserType(DjangoObjectType):
  class Meta:
    model = User
    exclude = ('is_superuser', 'is_staff', 'date_joined', 'password', 'is_active')


class UserInput(graphene.InputObjectType):
  username = graphene.String()
  email = graphene.String()
  bio = graphene.String()
  password = graphene.String()


class CreateUser(graphene.Mutation):
  class Arguments:
    user_input = UserInput(required=True)

  user = graphene.Field(UserType)

  @staticmethod
  def mutate(self, info, user_input=None):

    if test_db_connection(connections):
      user_instance = resolve_create_user(user_input)
      return CreateUser(user=user_instance)
    else:
      raise db_connection_error()

class DeleteUser(graphene.Mutation):

  deleted = graphene.Boolean()
  class Arguments:
    id = graphene.UUID()

  user = graphene.Field(UserType)

  @login_required
  def mutate(self, info, **kwargs):
    if test_db_connection(connections):
      logged_user_id = info.context.user.id

      deleted = resolve_delete_user(logged_user_id, kwargs)
      return DeleteUser(deleted=True)
    else:
      raise db_connection_error()

class UpdateUser(graphene.Mutation):

  class Arguments:
    id = graphene.UUID()
    user_input = UserInput(required=True)

  user = graphene.Field(UserType)
  @staticmethod
  def mutate(self, info, user_input=None, **kwargs):
    if test_db_connection(connections):
      logged_user_id = info.context.user.id
      user_instance = resolve_update_user(logged_user_id, user_input, kwargs)
      return UpdateUser(user=user_instance)

    else:
      raise db_connection_error()



class Query(graphene.ObjectType):
  users = graphene.List(UserType)
  user_by_id = graphene.Field(UserType, id=graphene.String())

  def resolve_users(self, info, **kwargs):
    if test_db_connection(connections):
      return User.objects.all()
    else:
      raise db_connection_error()

  def resolve_user_by_id(self, info, **kwargs):
    if test_db_connection(connections):
      return User.objects.get(pk=kwargs.get('id'))
    else:
      raise db_connection_error()


class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  delete_user = DeleteUser.Field()
  update_user = UpdateUser.Field()
