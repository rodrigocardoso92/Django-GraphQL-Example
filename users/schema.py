import graphene
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLError
from django.db import connections
from django.contrib.auth.hashers import make_password, check_password
import uuid
from users.models import User
from users.utils import test_db_connection

class UserType(DjangoObjectType):
  class Meta:
    model = User
    # fields = ('id', 'username', 'email', 'created_at', 'updated_at',)
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
      hashed_password = make_password(user_input.password)

      user_instance = User(
        id = uuid.uuid4(),
        username = user_input.username,
        email = user_input.email,
        bio = user_input.bio,
        password = hashed_password
      )

      user_instance.save()
      return CreateUser(user=user_instance)
    else:
      raise GraphQLError('DB Server not connected!')

class DeleteUser(graphene.Mutation):
  id = graphene.UUID()
  deleted = graphene.Boolean()
  class Arguments:
    id = graphene.UUID()
  
  user = graphene.Field(UserType)
  @staticmethod
  def mutate(self, info, **kwargs):
    if test_db_connection(connections):
      if not info.context.user.is_anonymous:
        user = User.objects.get(pk=kwargs.get('id'))

        user.delete()
        return DeleteUser(deleted=True)
      else:
        raise GraphQLError('You must be logged!')
    else:
      raise GraphQLError('DB Server not connected!')

class UpdateUser(graphene.Mutation):
  
  class Arguments:
    id = graphene.UUID()
    user_input = UserInput(required=True)

  user = graphene.Field(UserType)
  @staticmethod
  def mutate(self, info, user_input=None, **kwargs):
    if test_db_connection(connections):
      if not info.context.user.is_anonymous:
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

        return UpdateUser(user=user_instance)
      else:
        raise GraphQLError('You must be logged!')
    else:
      raise GraphQLError('DB Server not connected!')



class Query(graphene.ObjectType):
  users = graphene.List(UserType)
  user_by_id = graphene.Field(UserType, id=graphene.String())

  def resolve_users(self, info, **kwargs):
    if test_db_connection(connections):
      return User.objects.all()
    else:
      raise GraphQLError('DB Server not connected!')

  def resolve_user_by_id(self, info, **kwargs):
    if test_db_connection(connections):
      return User.objects.get(pk=kwargs.get('id'))
    else:
      raise GraphQLError('DB Server not connected!')


class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  delete_user = DeleteUser.Field()
  update_user = UpdateUser.Field()