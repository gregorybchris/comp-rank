import { makeQuery, makeURL, GET, POST, getSearchParams } from './request-util.js'
import { addKey, getKeys } from './storage-util.js'

new Vue({
    el: '.page',
    data: {
        topic: {},
        comparison: {},
        unlocked: false
    },
    methods: {
        goHome() {
            window.location.href = makeURL('/')
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
                this.fetchComparison()
                this.checkUnlocked()
            })
        },
        fetchComparison() {
            let params = {'topic_id': this.topic.id}
            GET(makeQuery('/comparison/next', params)).then(response => {
                console.log('Fetched Next Comparison: ', response.comparison)
                this.comparison = response.comparison
            })
        },
        submitComparison(winningItem) {
            let body = {
                'key': this.comparison.key,
                'winner_id': winningItem.id
            }
            POST(makeQuery('/comparison/submit'), body).then(response => {
                this.updateKeys()
                this.checkUnlocked()
                this.fetchComparison()
            })
        },
        updateKeys() {
            let updatedKeys = addKey(this.topic.id, this.comparison.key)
        },
        checkUnlocked() {
            let keys = getKeys(this.topic.id)
            let params = {
                'topic_id': this.topic.id,
                'keys': keys
            }
            POST(makeQuery('/rankings'), params).then(response => {
                if (this.unlocked != response.unlocked)
                    this.unlocked = response.unlocked
            })
        },
        viewRankings() {
            let params = {'topic': this.topic.id}
            let url = makeURL('/rankings.html', params)
            window.location.href = url
        }
    },
    created: function() {
        console.log('Vue Created: Compare')
        this.fetchData()
    }
})
