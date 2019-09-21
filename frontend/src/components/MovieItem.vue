<template>
  <div class="flex mt2 items-start">
    <div class="flex items-center">
      <span class="gray">{{movieNumber}}.</span>
      <div v-if="userId" class="ml1 gray f11 upvote" @click="voteForMovie()">▲</div>
    </div>
    <div class="ml1">
      <a :href="movie.title" class="movie">{{movie.description}} ({{movie.title}})</a>
      <div class="f6 lh-copy gray">
        {{movie.votes.length}} votes | by {{movie.postedBy ? movie.postedBy.username : 'Unknown'}} {{timeDifferenceForDate(movie.createdAt)}}
      </div>
    </div>
  </div>
</template>

<script>
  import { timeDifferenceForDate } from '../utils'
  import { ALL_MOVIES_QUERY, CREATE_VOTE_MUTATION } from '../constants/graphql'
  import { GC_USER_ID, MOVIES_PER_PAGE } from '../constants/settings'
  
  export default {
    name: 'MovieItem',
    data () {
      return {
        moviesPerPage: MOVIES_PER_PAGE
      }
    },
    computed: {
      userId () {
        return this.$root.$data.userId
      },
      movieNumber () {
        if (this.$route.path.includes('new')) {
          return (this.pageNumber - 1) * this.moviesPerPage + (this.index + 1)
        } else {
          return this.index + 1
        }
      }
    },
    props: ['movie', 'index', 'pageNumber'],
    methods: {
      timeDifferenceForDate,
      voteForMovie () {
        const userId = localStorage.getItem(GC_USER_ID)
        const voterIds = this.movie.votes.map(vote => vote.user.id)
        if (voterIds.includes(userId)) {
          alert(`User (${userId}) already voted for this movie.`)
          return
        }
        const movieId = this.movie.id
        this.$apollo.mutate({
          mutation: CREATE_VOTE_MUTATION,
          variables: {
            userId,
            movieId
          },
          update: (store, { data: { createVote } }) => {
            this.updateStoreAfterVote(store, createVote, movieId)
          }
        })
      },

      updateStoreAfterVote (store, createVote, movieId) {
        const data = store.readQuery({
          query: ALL_MOVIES_QUERY,
          variables: {     
            first: 5,
            skip: 0,
            orderBy: 'createdAt_DESC'
          }
        })
        const votedMovie = data.movies.find(movie => movie.id === movieId)
        votedMovie.votes = createVote.movie.votes
        store.writeQuery({ query: ALL_MOVIES_QUERY, data })
      }
    }
  }
</script>

<style scoped>
  .upvote {
    cursor: pointer;
  }

  .movie {
    text-decoration: none;
    color: black;
  }
</style>