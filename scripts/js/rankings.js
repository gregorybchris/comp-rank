import { makeQuery, makeURL, GET, POST, getSearchParams } from './request-util.js'
import { addKey, getKeys } from './storage-util.js'

new Vue({
    el: '.page',
    data: {
        topic: {},
        items: [],
        error: ''
    },
    methods: {
        goHome() {
            window.location.href = makeURL('/')
        },
        compareMore() {
            let params = {'topic': this.topic.id}
            let url = makeURL('/compare.html', params)
            window.location.href = url
        },
        fetchData() {
            let searchParams = getSearchParams()
            let topicID = searchParams.get('topic')
            //TODO: Do some frontend error if no parameter set
            //        or if this GET request returns an error
            let params = {'topic_id':topicID}
            GET(makeQuery('/topic', params)).then(response => {
                console.log('Fetched Topic: ', response.topic)
                this.topic = response.topic
                this.fetchRankings()
            })
        },
        fetchRankings() {
            let keys = getKeys(this.topic.id)
            let params = {
                'topic_id': this.topic.id,
                'keys': keys
            }
            POST(makeQuery('/rankings'), params).then(response => {
                if (response.unlocked) {
                    console.log('Items: ', response.items)
                    this.items = response.items
                }
                else
                    this.error = 'You need more comparisons to unlock these rankings'
            })
        }
    },
    created: function() {
        this.fetchData()
    }
})
