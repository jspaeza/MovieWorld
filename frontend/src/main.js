// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { ApolloLink } from 'apollo-link'
import Vue from 'vue'
import App from './App'
import router from './router'
import { GC_USER_ID, GC_AUTH_TOKEN } from './constants/settings'
import VueApollo from 'vue-apollo'
import { SubscriptionClient, addGraphQLSubscriptions } from 'subscriptions-transport-ws'
import 'tachyons'

Vue.config.productionTip = false

const httpLink = new HttpLink({
  // You should use an absolute URL here
  uri: 'http://localhost:8000/graphql/'
})

const wsClient = new SubscriptionClient('ws://localhost:5000', {
  reconnect: true,
  connectionParams: {
    authToken: localStorage.getItem(GC_AUTH_TOKEN)
  }
})

const authMiddleware = new ApolloLink((operation, forward) => {
  // add the authorization to the headers
  const token = localStorage.getItem(GC_AUTH_TOKEN)
  operation.setContext({
    headers: {
      Authorization: token ? `JWT ${token}` : null
    }
  })

  return forward(operation)
})

const httpLinkWithSubscriptions = addGraphQLSubscriptions(
  authMiddleware.concat(httpLink),
  wsClient
)

const apolloClient = new ApolloClient({
  link: httpLinkWithSubscriptions,
  cache: new InMemoryCache(),
  connectToDevTools: true
})

Vue.use(VueApollo)

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
  defaultOptions: {
    $loadingKey: 'loading'
  }
})

let userId = localStorage.getItem(GC_USER_ID)

new Vue({
  el: '#app',
  apolloProvider,
  router,
  data: {
    userId
  },
  render: h => h(App)
})
