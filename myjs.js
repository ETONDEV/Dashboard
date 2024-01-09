// myjs.js
function updateTime() {
    var now = new Date();
    document.getElementById('current-time').innerHTML = now.toLocaleTimeString();
    setTimeout(updateTime, 1000);
}

updateTime();
