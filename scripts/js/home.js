import { makeQuery, makeURL, GET } from './request-util.js'

new Vue({
    el: '.page',
    data: {
        categories: [],
    },
    methods: {
        goHome() {
            window.location.href = makeURL('/')
        },
        updateCategories() {
            GET(makeQuery('/categories')).then(response => {
                this.categories = response.categories
            })
        },
        topicClicked(topic) {
            let params = {'topic': topic.id}
            let url = makeURL('/compare.html', params)
            window.location.href = url
        }
    },
    created: function() {
        console.log('Vue Created: Home')
        this.updateCategories()
    }
})
