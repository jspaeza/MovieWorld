import Vue from 'vue'
import Router from 'vue-router'

import CreateMovie from '../components/CreateMovie'
import MovieList from '../components/MovieList'
import AppLogin from '../components/AppLogin'
import Search from '../components/Search'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MovieList',
      component: MovieList
    },
    {
      path: '/create',
      name: 'CreateMovie',
      component: CreateMovie
    },
    {
      path: '/login',
      component: AppLogin
    },
    {
      path: '/new/:page',
      component: MovieList
    },
    {
      path: '/search',
      component: Search
    },
    {
      path: '/top',
      component: MovieList
    }
  ],
  mode: 'history'
})
