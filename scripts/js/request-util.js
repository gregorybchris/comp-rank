//TODO: Set these by environment (local/heroku)
const API_ROOT = 'http://localhost:5000'
const FRONT_ROOT = 'http://localhost:8000'

const GET = async (url) => {
    let response = await fetch(url)
    let data = await response.json()
    return data
}

const POST = async (url, body) => {
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

const makeQuery = (endpoint, params={}) => {
    let noParamURL = API_ROOT + endpoint
    let paramURL = appendParams(noParamURL, params)
    return paramURL
}

const makeURL = (page, params={}) => {
    let noParamURL = FRONT_ROOT + page
    let paramURL = appendParams(noParamURL, params)
    return paramURL
}

const appendParams = (url, params) => {
    let fullURL = new URL(url)
    fullURL.search = new URLSearchParams(params)
    return fullURL.href
}

const getSearchParams = () => {
    return (new URL(location)).searchParams
}

export { makeQuery, makeURL, GET, POST, getSearchParams }
