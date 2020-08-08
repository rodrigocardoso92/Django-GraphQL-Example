import graphene

import post.schema
import users.schema

class Query(
  post.schema.Query,
  users.schema.Query,
  graphene.ObjectType
  ):
  pass

class Mutation(
  post.schema.Mutation,
  users.schema.Mutation,
  graphene.ObjectType
  ):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)