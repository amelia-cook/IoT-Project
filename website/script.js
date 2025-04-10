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
    // TODO: send POST request to Pi with new calendar ID
    // link: /addCalendar
    // data: cal
}

function newSubmit() {
    stickyName = document.getElementById("name").value;
    stickyContent = document.getElementById("newContent").value;
    // TODO: send POST request to Pi with new sticky
    // link: /newSticky
    // data: name, content
}

function nameSubmit() {
    stickyName = document.getElementById("name").value;
    
    // TODO: send GET request to Pi for sticky content
    // link: /getSticky?name=stickyName
    
    updateWithSticky();
}

function updateWithSticky() {
    // TODO: fill with contents of sticknote
    // document.getElementById("newContent").value = 
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
    xhr.open("POST", link, true);
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