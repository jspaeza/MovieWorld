import gql from 'graphql-tag'

export const ALL_MOVIES_QUERY = gql`
  query AllMoviesQuery($first: Int, $skip: Int, $orderBy: MovieOrderBy) {
    movies(first: $first, skip: $skip, orderBy: $orderBy) {
      id
      title
      description
      postedBy {
        id
        username
      }
      votes {
        id
        user {
          id
        }
      }  
    }
    _allMoviesMeta {
      count
    }
  }
`

export const CREATE_MOVIE_MUTATION = gql`
  mutation CreateMovieMutation($description: String!, $title: String!) {
    createMovie(
      description: $description,
      title: $title,
    ) {
      id
      title
      description
    }
  }
`

export const CREATE_USER_MUTATION = gql`
  mutation ($username: String!, $email: String!, $password: String!) {
    createUser(
      username: $username,
      password: $password,
      email: $email  
    ) {
      user {
        id
      }
    }

    tokenAuth(username: $username, password: $password) {
      token
      user {
        id
      }
    }
  }
`

export const SIGNIN_USER_MUTATION = gql`
  mutation ($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
      user {
        id
      }
    }
  }
`

export const CREATE_VOTE_MUTATION = gql`
  mutation($movieId: Int!) {
    createVote(movieId: $movieId) {
      movie {
        votes {
          id
          user {
            id
          }
        }
      }
      user {
        id
      }
    }    
  }
`

export const ALL_MOVIES_SEARCH_QUERY = gql`
  query AllMoviesSearchQuery($searchText: String!) {
    movies(search: $searchText) {
      id
      title
      description
      postedBy {
        id
        username
      }
      votes {
        id
        user {
          id
        }
      }
    }
  }
`

export const NEW_MOVIES_SUBSCRIPTION = gql`
  subscription {
    Movie(filter: {
      mutation_in: [CREATED]
    }) {
      node {
        id
        title
        description
        createdAt
        postedBy {
          id
          name
        }
        votes {
          id
          user {
            id
          }
        }
      }
    }
  }
`