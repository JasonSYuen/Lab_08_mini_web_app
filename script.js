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
            console.log(ourData.password)
            console.log(password)
            if (password == ourData.password) {
                console.log(ourData.Student_Teacher_Admin)
                if (ourData.Student_Teacher_Admin == "student") {
                    alert("student")
                    window.location.href = "student.html";
                }
                if (ourData.Student_Teacher_Admin == "admin") {
                    //const adminUrl = document.getElementById("admin-url").value;
                    //document.getElementById("admin-url").style.type = ""
                    window.location.href = "http://127.0.0.1:5000/admin/username_password";
                }

            }
            else {
                alert("incorrect password")
            }

        }
        request.send();

    });
}
