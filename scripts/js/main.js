const get = async (endpoint) => {
    let root = 'http://localhost:5000'
    let response = await fetch(root + endpoint)
    let data = await response.json()
    return data
}

let hello = new Vue({
    el: '.hello',
    data: {
        message: ''
    },
    methods: {
        update() {
            get('/').then(response => {
                this.message = response.message
            })
        }
    },
    created: function() {
        this.update()
    }
})
