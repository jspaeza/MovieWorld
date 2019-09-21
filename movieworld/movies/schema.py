import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q #Queries complejas 

from movies.models import Movie, Vote
from users.schema import UserType

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    movies = graphene.List(
        MovieType, 
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
        )
    votes = graphene.List(VoteType)

    def resolve_movies(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Movie.objects.all()
        
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(genero__icontains=search)
            )
            qs = qs.filter(filter)
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#Mutations
class CreateMovie(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    director = graphene.String()
    genero = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        director = graphene.String()
        genero = graphene.String()
    
    def mutate(self, info, title, description, director, genero):
        user = info.context.user or None

        movie = Movie(title=title, description=description, director=director, 
                genero=genero)
        movie.save()

        return CreateMovie(
            id=movie.id,
            title=movie.title,
            description=movie.description,
            director=movie.director,
            genero=movie.genero,
            posted_by=movie.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    movie = graphene.Field(MovieType)

    class Arguments:
        movie_id = graphene.Int()

    def mutate(self, info, movie_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        movie = Movie.objects.filter(id = movie_id).first()
        if not movie:
            raise Exception('Invalid Movie!')

        Vote.objects.create(
            user = user,
            movie = movie,
        )

        return CreateVote(user = user, movie = movie)
    
class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    create_vote = CreateVote.Field()