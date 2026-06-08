import graphene
import educlubs.schema

class Query(educlubs.schema.Query, graphene.ObjectType):
    pass

class Mutation(educlubs.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
