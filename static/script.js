
var defintion_box = document.getElementById('definition')

async function getDef(word) {
    // TODO: REMOVE THE API KEY FROM THE CALL HERE 
    // https://www.dictionaryapi.com/api/v3/references/collegiate/json/test?key=325142d6-6793-4d6f-8f67-8b23d76755e0
    // https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=your-api-key
    let resp = await fetch("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=325142d6-6793-4d6f-8f67-8b23d76755e0");
    let dict_resp = await resp.json();
    let definition = dict_resp[0]['def'];
    console.log(definition);
    document.getElementById('definition').innerHTML = "<h3>" + word + "</h3><br>" + definition;
    document.getElementById('definition').classList.toggle("visible");

}

window.onclick = function (event) {
    if (event.target == defintion_box) {
        defintion.style.visibility = "none";
    }
}
