import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Movie


#1
class MovieFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'genero']


#2
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        #3
        interfaces = (graphene.relay.Node, )


class RelayQuery(graphene.ObjectType):
    #4
    relay_movie = graphene.relay.Node.Field(MovieNode)
    #5
    relay_movies = DjangoFilterConnectionField(MovieNode, filterset_class=MovieFilter)


class RelayCreateMovie(graphene.relay.ClientIDMutation):
    movie = graphene.Field(MovieNode)

    class Input:
        title = graphene.String()
        description = graphene.String()
        director = graphene.String()
        genero = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        movie = movie(
            title=input.get('title'),
            description=input.get('description'),
            director=input.get('director'),
            genero=input.get('genero'),
            posted_by=user,
        )
        movie.save()

        return RelayCreateMovie(movie=movie)


class RelayMutation(graphene.AbstractType):
    relay_create_movie = RelayCreateMovie.Field()