import graphene
import graphql_jwt

import movies.schema
import users.schema
import movies.schema_relay

class Query(users.schema.Query, movies.schema.Query, movies.schema_relay.RelayQuery, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, movies.schema.Mutation, movies.schema_relay.RelayMutation, graphene.ObjectType,):
    #token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    token_auth = users.schema.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)