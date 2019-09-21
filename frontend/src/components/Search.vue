<template>
  <div>
    <div>
      Search
      <!-- 1 -->
      <input type="text" v-model="searchText">
    </div>
    <movie-item
      v-for="(movie, index) in movies"
      :key="movie.id"
      :movie="movie"
      :index="index">
    </movie-item>
  </div>
</template>

<script>
  // 2
  import { ALL_MOVIES_SEARCH_QUERY } from '../constants/graphql'
  import MovieItem from './MovieItem'

  export default {
    name: 'Search',
    data () {
      return {
        movies: [],
        searchText: ''
      }
    },
    // 3
    apollo: {
      movies: {
        query: ALL_MOVIES_SEARCH_QUERY,
        variables () {
          return {
            searchText: this.searchText
          }
        },
        skip () {
          return !this.searchText
        }
      }
    },
    components: {
      MovieItem
    }
  }
</script>