export class Student {
    firstName: string
    middleInitial: string
    lastName: string

    constructor(firstName: string, middleInitial: string, lastName: string) {
        this.firstName = firstName
        this.middleInitial = middleInitial
        this.lastName = lastName
    }

    fullName(): string {
        return this.firstName + " " + this.middleInitial + " " + this.lastName
    }
}
