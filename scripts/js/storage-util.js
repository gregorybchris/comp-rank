const KEY_STORE_NAME = 'comp-rank-keys'

const getAllKeys = () => {
    let local = window.localStorage
    if (local.getItem(KEY_STORE_NAME) === null)
        local.setItem(KEY_STORE_NAME, JSON.stringify({}))
    let keysString = local.getItem(KEY_STORE_NAME)
    let allKeys = JSON.parse(keysString)
    return allKeys
}

const clearAllKeys = () => {
    let local = window.localStorage
    local.setItem(KEY_STORE_NAME, JSON.stringify({}))
}

const saveAllKeys = (keys) => {
    let newKeysString = JSON.stringify(keys)
    let local = window.localStorage
    local.setItem(KEY_STORE_NAME, newKeysString)
}

const addKey = (topicID, key) => {
    let allKeys = getAllKeys()
    if (!(topicID in allKeys))
        allKeys[topicID] = []
    let topicKeys = allKeys[topicID]
    topicKeys.push(key)
    saveAllKeys(allKeys)
    return topicKeys
}

const getKeys = (topicID) => {
    let allKeys = getAllKeys()
    let topicKeys = allKeys[topicID]
    if (!topicKeys)
        return []
    return topicKeys
}

export { addKey, getKeys }
