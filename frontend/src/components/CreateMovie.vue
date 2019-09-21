<template>
  <div>
    <div class="flex flex-column mt3">
      <input
        class="mb2"
        v-model="description"
        type="text"
        placeholder="A description for the movie">
      <input
        class="mb2"
        v-model="title"
        type="text"
        placeholder="The title for the movie">
    </div>
    <button @click="createMovie()">Submit</button>
  </div>
</template>

<script>
    import { ALL_MOVIES_QUERY, CREATE_MOVIE_MUTATION } from '../constants/graphql'

    export default {
        name: 'CreateMovie',
        data () {
            return {
                description: '',
                title: ''
            }
        },
        methods: {
            createMovie () {
                const { description, title } = this.$data
                this.$apollo.mutate({
                    mutation: CREATE_MOVIE_MUTATION,
                    variables: {
                        description,
                        title
                    },
                    update: (store, { data: { createMovie } }) => {
                        const data = store.readQuery({
                            query: ALL_MOVIES_QUERY,
                            variables: {
                                first: 5,
                                skip: 0,
                                orderBy: 'createdAt_DESC'
                            }
                        })
                        data.movies.push(createMovie)
                        store.writeQuery({ 
                            query: ALL_MOVIES_QUERY, 
                            variables: {
                                first: 5,
                                skip: 0,
                                orderBy: 'createdAt_DESC'
                            },
                            data 
                        })
                    } 
                }).then((data) => {
                    this.$router.push({path: '/'})
                }).catch((error) => {
                    console.error(error)
                })
            }
        }
    }
</script>