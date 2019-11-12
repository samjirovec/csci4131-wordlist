
var defintion_box = document.getElementById("definition");


async function getDef(word) {
    var close_message = "<button class='exit' onclick='goInvis()'> Click Here to Close </button>";
    var host = window.location.hostname;
    console.log(host);
    var resp = await fetch('/def/' + word);
    var def = await resp.json();
    console.log(def);
    if(def.length != 0){
        document.getElementById('definition').innerHTML = "<b>" + word + "</b> : " + def  + "<br>" + close_message;
    }
    else {
        document.getElementById('definition').innerHTML = "<b>" + word + "</b> : " + "No Def Available" + "<br>" + close_message;
    }
    document.getElementById('definition').style.display = "block";
}


function goInvis() {
    document.getElementById('definition').style.display = "none";
    console.log("HERE")
}
