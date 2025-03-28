import graphene
import GraphAPI.schema


class Query(GraphAPI.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
