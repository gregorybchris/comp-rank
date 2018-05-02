var Student = (function () {
    function Student(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
    }
    Student.prototype.fullName = function () {
        return this.firstName + " " + this.middleInitial + " " + this.lastName;
    };
    return Student;
}());
function greeter(person) {
    return "Hello, " + person.fullName();
}
var user = new Student("Jane", "M", "Franklin");
var text = document.getElementById("text");
text.innerHTML = greeter(user);
