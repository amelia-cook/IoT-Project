function onLoad() {
    ipaddr = sessionStorage.getItem("ipaddr");
    if (ipaddr != null) {
        document.getElementById("ipaddr").value = ipaddr;
    }
    
    if (document.getElementById("hide")) { 
        if (sessionStorage.getItem("hidden?") == "hidden") {
            document.getElementById("hide").value = "Show Display";
        } else {
            document.getElementById("hide").value = "Hide Display";
        }
    }
}

function ipSubmit() {
    addr = document.getElementById("ipaddr");
    sessionStorage.setItem("ipaddr", addr.value);
}

function calSubmit() {
    cal = document.getElementById("calID").value;
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    link = "http://" + ipaddr + ":5000/calID";
    
    data = new Object();
    data.calID = cal;
    
    apiPOST(link, JSON.stringify(data));
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
    
    apiPOST(link, JSON.stringify(data));
}

function nameSubmit() {
    stickyName = document.getElementById("name").value;
    
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    
    link = "http://" + ipaddr + ":5000/getSticky?name=" + stickyName;
    apiGET(link);
}

function removeSubmit() {
    stickyName = document.getElementById("name").value;
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    
    link = "http://" + ipaddr + ":5000/removeSticky?name=" + stickyName;
    apiGET(link);
}

function display() {
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    
    link = ""
    
    if (sessionStorage.getItem("hidden?") == "hidden") {
        sessionStorage.setItem("hidden?", "shown");
        document.getElementById("hide").value = "Hide Display";
        
        link = "http://" + ipaddr + ":5000/show";
    } else {
        sessionStorage.setItem("hidden?", "hidden");
        document.getElementById("hide").value = "Show Display";
        
        link = "http://" + ipaddr + ":5000/hide";
    }
    
    apiGET(link);
}

function clear_stickies() {
    ipaddr = sessionStorage.getItem("ipaddr");
    if (!ipaddr) {
        alert("Please enter IP Address");
        return;
    }
    
    link = "http://" + ipaddr + ":5000/clear";
    apiGET(link);
}

function updateTextBox(text) {
    document.getElementById("newContent").value = text;
}

function apiGET(link) { 
    xhr = new XMLHttpRequest();
    if (!xhr) {
        alert("Unable to create HTTPRequest object");
        return;
    }
    xhr.open("GET", link, false);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Changing string data into JSON Object
            obj = JSON.parse(this.responseText);
            
            updateTextBox(obj.content);
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
            
            response = this.ResponseText;
        }
        else {
            console.log("File not found");
        }
    }
    xhr.send(data);
}
