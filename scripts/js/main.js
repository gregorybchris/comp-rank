const ROOT = 'http://localhost:5000'

const get = async (url) => {
    let response = await fetch(url)
    let data = await response.json()
    return data
}

const post = async (url, body) => {
    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(body),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    })
    let data = await response.json()
    return data
}

const appendParams = (url, params) => {
    let fullURL = new URL(url)
    fullURL.search = new URLSearchParams(params)
    return fullURL.href
}

new Vue({
    el: '.page',
    data: {
        categories: [],
        topic: {},
        comparison: {},
        selecting: true,
        comparing: false,
        ranking: false
    },
    methods: {
        switchView(view) {
            this.selecting = false
            this.comparing = false
            this.ranking = false
            if (view == 'selecting')
                this.selecting = true
            else if (view == 'comparing')
                this.comparing = true
            else if (view == 'ranking')
                this.ranking = true
        },
        updateCategories() {
            get(ROOT + '/categories').then(response => {
                this.categories = response.categories
            })
        },
        topicClicked(topic) {
            console.log('Topic Clicked: ', topic.name)
            this.topic = topic
            this.nextComparison()
        },
        nextComparison() {
            let params = {'topic_id': this.topic.id}
            let query = appendParams(ROOT + '/comparison/next', params)
            get(query).then(response => {
                console.log('Fetched Next Comparison: ', response.comparison)
                this.comparison = response.comparison
                this.switchView('comparing')
            })
        },
        submitComparison(winningItem) {
            console.log('Chose: ', winningItem.name, '(' + winningItem.id + ')')
            let body = {
                'key': this.comparison.key,
                'past_keys': [],
                'winner_id': winningItem.id
            }
            post(ROOT + '/comparison/submit', body).then(response => {
                let unlocked = response.unlocked
                console.log('Submitted Comparison: ', '(unlocked=' + unlocked + ')')
            })
            this.nextComparison()
        }
    },
    created: function() {
        this.updateCategories()
    }
})
