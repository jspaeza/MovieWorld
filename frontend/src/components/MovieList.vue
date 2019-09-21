<template>
  <div>
    <div>
      <movie-item
        v-for="(movie, index) in orderedMovies"
        :key="movie.id"
        :movie="movie"
        :index="index"
        :pageNumber="pageNumber">
      </movie-item>
    </div>
    <div v-if="isNewPage">
      <button v-show="!isFirstPage" @click="previousPage()">Previous</button>
      <button v-show="morePages" @click="nextPage()">Next</button>
    </div>
  </div>
</template>

<script>
  import { ALL_MOVIES_QUERY, NEW_MOVIES_SUBSCRIPTION } from '../constants/graphql'
  import MovieItem from './MovieItem'
  import { MOVIES_PER_PAGE } from '../constants/settings'
  import _ from 'lodash'

  export default {
    name: 'MovieList',
    data () {
      return {
        movies: [],
        count: 0,
        loading: 0
      }
    },
    components: {
      MovieItem
    },

    methods: {
      getMoviesToRender (isNewPage) {
        if (isNewPage) {
          return this.$apollo.queries.movies
        }
        const rankedMovies = this.$apollo.queries.movies.slice()
        rankedMovies.sort((l1, l2) => l2.votes.length - l1.votes.length)
        return rankedMovies
      },
      nextPage () {
        const page = parseInt(this.$route.params.page, 10)
        if (page < this.count / MOVIES_PER_PAGE) {
          const nextPage = page + 1
          this.$router.push({path: `/new/${nextPage}`})
        }
      },
      previousPage () {
        const page = parseInt(this.$route.params.page, 10)
        if (page > 1) {
          const previousPage = page - 1
          this.$router.push({path: `/new/${previousPage}`})
        }
      }
    },

    computed: {
      orderedMovies: function () {
        if (this.$route.path.includes('top')) {
          return _.orderBy(this.movies, 'votes.length').reverse()
        } else {
          return this.movies
        }
      },
      isFirstPage () {
        return this.$route.params.page === '1'
      },
      isNewPage () {
        return this.$route.path.includes('new')
      },
      pageNumber (index) {
        return parseInt(this.$route.params.page, 10)
      },
      morePages () {
        return parseInt(this.$route.params.page, 10) < this.count / MOVIES_PER_PAGE
      }
    },
    apollo: {
      variables () {
        const page = parseInt(this.$route.params.page, 10)
        const isNewPage = this.$route.path.includes('new')
        const skip = isNewPage ? (page - 1) * MOVIES_PER_PAGE : 0
        const first = isNewPage ? MOVIES_PER_PAGE : 100
        const orderBy = isNewPage ? 'createdAt_DESC' : null
        return {
          first,
          skip,
          orderBy
        }
      },

      update (data) {
        this.count = data._allMoviesMeta.count
        return data.movies
      },

      movies: {
        query: ALL_MOVIES_QUERY
      },

      subscribeToMore: [
        {
          document: NEW_MOVIES_SUBSCRIPTION,
          updateQuery: (previous, { subscriptionData }) => {
            const newAllMovies = [
              subscriptionData.data.Movie.node,
              ...previous.movies
            ]
            const result = {
              ...previous,
              movies: newAllMovies.slice(0, MOVIES_PER_PAGE)
            }
            return result
          }
        }
      ]
    }
  }
</script>