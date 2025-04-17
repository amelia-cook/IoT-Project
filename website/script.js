APIKEY = "AIzaSyCPYurU7oRoK0nYeFll2Y5sS3oGY2VLgWM"
response = ""

function onLoad() {
    ipaddr = sessionStorage.getItem("ipaddr");
    if (ipaddr != null) {
        document.getElementById("ipaddr").value = ipaddr;
    }
}

function ipSubmit() {
    addr = document.getElementById("ipaddr");
    sessionStorage.setItem("ipaddr", addr.value);
    // alert(addr.value + "\n" + sessionStorage.getItem("ipaddr"));
}

function calSubmit() {
    cal = document.getElementById("calID").value;
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    link = "http://" + ipaddr + ":5000/calID";
    // alert(link + " " + cal);
    apiPOST(link, cal);
}

function newSubmit() {
    stickyName = document.getElementById("name").value;
    stickyContent = document.getElementById("newContent").value;
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    link = "http://" + ipaddr + ":5000/createSticky";
    
    data = new Object();
    data.name = stickyName;
    data.content = stickyContent;
    
    // alert(link + " " + JSON.stringify(data));
    
    apiPOST(link, JSON.stringify(data));
}

function nameSubmit() {
    stickyName = document.getElementById("name").value;
    
    alert(stickyName);
    
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    
    link = "http://" + ipaddr + ":5000/getSticky?name=" + stickyName;
    apiGET(link);
    
    if (response != "") {
        document.getElementById("newContent").value = response;
        response = "";
    }
}

function apiGET(link) {
    xhr = new XMLHttpRequest();
    if (!xhr) {
        alert("Unable to create HTTPRequest object");
        return;
    }
    xhr.open("GET", link, true);
    xhr.onload = function () {
        if (this.status === 200) {
            // Changing string data into JSON Object
            obj = JSON.parse(this.responseText);
            
            alert(this.responseText);
            response = this.ResponseText;
        }
        else {
            console.log("File not found");
        }
    }
    xhr.send();
}

function apiPOST(link, data) {
    xhr = new XMLHttpRequest();
    if (!xhr) {
        alert("Unable to create HTTPRequest object");
        return;
    }
    xhr.open("POST", link);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
        if (this.status === 200) {
            // Changing string data into JSON Object
            obj = JSON.parse(this.responseText);
            
            alert(this.responseText);
            response = this.ResponseText;
        }
        else {
            console.log("File not found");
        }
    }
    xhr.send(data);
}

// curl -i -X GET -H "X-goog-api-key: APIKEY" https://www.googleapis.com/calendar/v3/calendars/stickynoteiot@gmail.com/events

// sessionStorage.setItem(KEY, VALUE)
// sessionStorage.getItem(KEY)
// sessionStorage.removeItem(KEY)
// sessionStorage.clear()