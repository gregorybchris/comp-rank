import { Student } from "./student.js"

declare var fetch;

function greeter(person: Student) {
    return "Hello, " + person.fullName()
}

let user = new Student("Jane", "M", "Franklin")

console.log("User: ", user, greeter(user))

let textElement = document.getElementById("text")

async function getData() {
    let response = await fetch('https://localhost:5000/')
    let data = await response.json()
    return data
}


getData().then(function(data) {
    textElement.innerHTML = data
})
