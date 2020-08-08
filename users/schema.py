import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.hashers import make_password, check_password
import uuid
from users.models import User

class UserType(DjangoObjectType):
  class Meta:
    model = User


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


class Query(graphene.ObjectType):
  users = graphene.List(UserType)
  user_by_id = graphene.Field(UserType, id=graphene.String())

  def resolve_users(self, info, **kwargs):
    return User.objects.all()

  def resolve_user_by_id(self, info, **kwargs):
    return User.objects.get(pk=kwargs.get('id'))


class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()