
const loaded = document.getElementById('login');
if (loaded) {
    document.getElementById("login").addEventListener("submit", function (event) {
        event.preventDefault()
        console.log("Function Called")
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        var request = new XMLHttpRequest();
        let string = "http://127.0.0.1:5000/login/" + username;
        request.open('GET', string);
        request.onload = function () {
            //const ourData = JSON.parse(request.responseText);
            const ourData = JSON.parse(request.responseText);
            console.log()
            console.log(password)
            console.log(request.responseText)

            if (password == ourData.password && ourData.not_found == false) {
                console.log(ourData.username)
                //const l = document.getElementById('myName');
                //document.getElementById('myName').innerHTML = ourData.username
                //myNameObj.myName = ourData.username
                var r = new XMLHttpRequest();
                r.open('POST', "http://127.0.0.1:5000/store/" + username);
                r.onload = function () { }
                r.send();

                //console.log("my: " + myNameObj.myName)
                console.log(ourData.Student_Teacher_Admin)
                if (ourData.Student_Teacher_Admin == "student") {

                    window.location.href = "student.html";
                }
                if (ourData.Student_Teacher_Admin == "admin") {
                    //const adminUrl = document.getElementById("admin-url").value;
                    //document.getElementById("admin-url").style.type = ""
                    window.location.href = "http://127.0.0.1:5000/admin/username_password";
                }
                if (ourData.Student_Teacher_Admin == "teacher") {

                    window.location.href = "teacherpage.html";
                }

            }
            else {
                alert("incorrect password or username")
            }

        }
        request.send();

    });
}

function showMy() {

    var myName;

    var r = new XMLHttpRequest();
    r.open('GET', "http://127.0.0.1:5000/store");
    r.onload = function () {
        myName = r.responseText

        console.log("a: " + myName)
        var request = new XMLHttpRequest();
        let string = "http://127.0.0.1:5000/studentdata/" + myName;
        console.log("s: " + string)
        request.open('GET', string);
        request.onload = function () {
            const ourData = JSON.parse(request.responseText);

            //console.log(ourData)

            //document.getElementById("myClasses").innerText += ourData
            tbl = document.getElementById("student_myClasses");
            console.log(tbl.rows.length)
            let size = tbl.rows.length;
            for (j = 1; j < size; j = j + 1) {
                tbl.deleteRow(1);
                console.log(j)
            }
            Count = 0;
            for (y in ourData) {
                const tr = tbl.insertRow();
                const td = tr.insertCell();
                const td2 = tr.insertCell();
                const td3 = tr.insertCell();
                const td4 = tr.insertCell();
                const td5 = tr.insertCell();
                const td6 = tr.insertCell();

                td.appendChild(document.createTextNode((ourData[Count].Class)))
                td2.appendChild(document.createTextNode((ourData[Count].Teacher_Name)))
                td3.appendChild(document.createTextNode((ourData[Count].Time)))
                td4.appendChild(document.createTextNode((ourData[Count].Capacity)))
                td5.appendChild(document.createTextNode((ourData[Count].Students_Enrolled)))
                td6.appendChild(document.createTextNode((ourData[Count].Class_id)))
                Count += 1
                //console.log(y)
            }
        }
        request.send();


    }

    r.send();

    //myName = document.getElementById('myName').innerHTML


}

function showAll() {

    var myName;

    var r = new XMLHttpRequest();
    r.open('GET', "http://127.0.0.1:5000/store");
    r.onload = function () {
        myName = r.responseText

        console.log("a: " + myName)
        var request = new XMLHttpRequest();
        let string = "http://127.0.0.1:5000/allcourses";
        console.log("s: " + string)
        request.open('GET', string);
        request.onload = function () {
            const ourData = JSON.parse(request.responseText);
            console.log(ourData)
            //document.getElementById("allClasses").innerText += ourData
            tbl = document.getElementById("student_allClasses");
            console.log(tbl.rows.length)
            let size = tbl.rows.length;
            for (j = 1; j < size; j = j + 1) {
                tbl.deleteRow(1);
                console.log(j)
            }
            Count = 0;
            for (y in ourData) {
                const tr = tbl.insertRow();
                const td = tr.insertCell();
                const td2 = tr.insertCell();
                const td3 = tr.insertCell();
                const td4 = tr.insertCell();
                const td5 = tr.insertCell();
                const td6 = tr.insertCell();

                td.appendChild(document.createTextNode((ourData[Count].Class)))
                td2.appendChild(document.createTextNode((ourData[Count].Teacher_Name)))
                td3.appendChild(document.createTextNode((ourData[Count].Time)))
                td4.appendChild(document.createTextNode((ourData[Count].Capacity)))
                td5.appendChild(document.createTextNode((ourData[Count].Students_Enrolled)))
                td6.appendChild(document.createTextNode((ourData[Count].Class_id)))
                Count += 1
                //console.log(y)
            }

        }
        request.send();


    }

    r.send();

    //myName = document.getElementById('myName').innerHTML




}

const loaded2 = document.getElementById('deleteClass')
if (loaded2) {

    document.getElementById("deleteClass").addEventListener("submit", function (event) {
        event.preventDefault()
        console.log("a");
        var myName;

        var r = new XMLHttpRequest();
        r.open('GET', "http://127.0.0.1:5000/store");
        r.onload = function () {
            myName = r.responseText

            let id = document.getElementById("delete").value;
            let string = "http://127.0.0.1:5000/delete/" + id + "/" + myName;
            var request = new XMLHttpRequest();
            request.open('DELETE', string);
            request.onload = function () {
                const ourData = (request.responseText);
                console.log(ourData)
                document.getElementById("indv").innerText += ourData
            }
            request.send();
            // console.log("a")


        }
        r.send();
    }

    )
}

const loaded3 = document.getElementById('addClass')
if (loaded3) {

    document.getElementById("addClass").addEventListener("submit", function (event) {
        event.preventDefault()
        console.log("a");
        var myName;

        var r = new XMLHttpRequest();
        r.open('GET', "http://127.0.0.1:5000/store");
        r.onload = function () {
            myName = r.responseText

            let id = document.getElementById("add").value;
            let string = "http://127.0.0.1:5000/add/" + id + "/" + myName;
            var request = new XMLHttpRequest();
            request.open('POST', string);
            request.onload = function () {
                alert(request.responseText)
            }
            // console.log("a")
            request.send();

        }
        r.send();
    }

    )
}


function showMyClasses() {
    var myName;

    var r = new XMLHttpRequest();
    r.open('GET', "http://127.0.0.1:5000/store");
    r.onload = function () {
        myName = r.responseText

        console.log("a: " + myName)
        var request = new XMLHttpRequest();
        let string = "http://127.0.0.1:5000/mycourses/" + myName;
        console.log("s: " + string)
        request.open('GET', string);
        request.onload = function () {
            const ourData = JSON.parse(request.responseText);
            console.log(ourData)
            //document.getElementById("myClasses").innerText += ourData
            tbl = document.getElementById("myClassesTable");
            console.log(tbl.rows.length)
            let size = tbl.rows.length;
            for (j = 1; j < size; j = j + 1) {
                tbl.deleteRow(1);
                console.log(j)
            }
            Count = 0;
            for (y in ourData) {
                const tr = tbl.insertRow();
                const td = tr.insertCell();
                const td2 = tr.insertCell();
                const td3 = tr.insertCell();
                const td4 = tr.insertCell();
                const td5 = tr.insertCell();
                const td6 = tr.insertCell();

                td.appendChild(document.createTextNode((ourData[Count].Class)))
                td2.appendChild(document.createTextNode((ourData[Count].Teacher_Name)))
                td3.appendChild(document.createTextNode((ourData[Count].Time)))
                td4.appendChild(document.createTextNode((ourData[Count].Capacity)))
                td5.appendChild(document.createTextNode((ourData[Count].Students_Enrolled)))
                td6.appendChild(document.createTextNode((ourData[Count].Class_id)))
                Count += 1
                //console.log(y)
            }
        }
        request.send();


    }

    r.send();

    //myName = document.getElementById('myName').innerHTML
}

var ThisClassID;
const loaded4 = document.getElementById('indvClass')
if (loaded4) {

    document.getElementById("indvClass").addEventListener("submit", function (event) {
        event.preventDefault()
        console.log("a");
        var myName;

        var r = new XMLHttpRequest();
        r.open('GET', "http://127.0.0.1:5000/store");
        r.onload = function () {
            myName = r.responseText

            let id = document.getElementById("indvClassInput").value;
            ThisClassID = id
            console.log(id)
            let string = "http://127.0.0.1:5000/indvcourse/" + myName + "/" + id;
            var request = new XMLHttpRequest();
            request.open('GET', string);
            request.onload = function () {
                const ourData = JSON.parse(request.responseText);
                console.log(ourData)
                //document.getElementById("indvClasses").innerText += ourData

                tbl = document.getElementById("myStudent");
                console.log(tbl.rows.length)
                let size = tbl.rows.length;
                for (j = 1; j < size; j = j + 1) {
                    tbl.deleteRow(1);
                    console.log(j)
                }
                Count = 0;
                for (y in ourData) {
                    const tr = tbl.insertRow();
                    const td = tr.insertCell();
                    const td2 = tr.insertCell();
                    //const td3 = tr.insertCell();
                    //const td4 = tr.insertCell();
                    //const td5 = tr.insertCell();

                    td.appendChild(document.createTextNode((ourData[Count].name)))
                    td2.appendChild(document.createTextNode((ourData[Count].Grade)))
                    //td3.appendChild(document.createTextNode((ourData[Count].Time)))
                    //td4.appendChild(document.createTextNode((ourData[Count].Capacity)))
                    //td5.appendChild(document.createTextNode((ourData[Count].Students_Enrolled)))
                    Count += 1
                    //console.log(y)
                }
            }
            request.send();

        }
        r.send();
    }
    )
}


const loaded6 = document.getElementById('editGrade');
if (loaded6) {
    document.getElementById("editGrade").addEventListener("submit", function (event) {
        event.preventDefault()
        console.log("Function Called")
        let student_name = document.getElementById("studentName").value;
        let student_grade = document.getElementById("studentGrade").value;

        let string = "http://127.0.0.1:5000/editGrade/" + student_name + "/" + ThisClassID + "/" + student_grade;
        var request = new XMLHttpRequest();
        request.open('POST', string);
        request.onload = function () {
            //const ourData = JSON.parse(request.responseText);
            console.log("done")

        }
        request.send()



    });
}

function getName() {
    var r = new XMLHttpRequest();
    r.open('GET', "http://127.0.0.1:5000/store");
    r.onload = function () {
        if (r.status === 200) {
            var username = r.responseText; // Retrieve the username
            document.getElementById("welcome").textContent = "Welcome, " + username; // Update the welcome message
        } else {
            console.error("Failed to retrieve username");
        }
    };
    r.send();
}


window.onload = getName;