import graphene
import graphql_jwt

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
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
  delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)