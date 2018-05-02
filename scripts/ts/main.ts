class Student {
    firstName: string;
    middleInitial: string;
    lastName: string;

    constructor(firstName: string, middleInitial: string, lastName: string) {
        this.firstName = firstName
        this.middleInitial = middleInitial
        this.lastName = lastName
    }

    fullName(): string {
        return this.firstName + " " + this.middleInitial + " " + this.lastName
    }
}

function greeter(person: Student) {
    return "Hello, " + person.fullName()
}

let user = new Student("Jane", "M", "Franklin");

let text = document.getElementById("text")
text.innerHTML = greeter(user)
