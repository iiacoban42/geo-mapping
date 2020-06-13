
 function resizeIframe(){
    var iframe = document.getElementsByClassName("frame")[0];
    
    //iframe.style.height = '0 px';
    iframe.style.height = (iframe.contentWindow.document.body.scrollHeight + 10) + 'px';
 }

window.onload = function() {
    var captcha_div = document.getElementById("captcha")

    var uuid_input = document.createElement("input")
    uuid_input.setAttribute("id", "uuid_input");
    uuid_input.setAttribute("name", "captcha_uuid");
    uuid_input.setAttribute("type", "hidden");

    var iframe = document.createElement("iframe")
    iframe.setAttribute("src", "/captcha_embed");
    iframe.setAttribute("sandbox", "allow-forms allow-scripts allow-same-origin");
    iframe.setAttribute("frameBorder", "0");
    iframe.setAttribute("scrolling", "no");
    iframe.setAttribute("id", "frame");
    iframe.setAttribute("style", "width: 100%; height: auto; position: absolute; z-index: 9999;");
    iframe.classList.add("frame")

    captcha_div.appendChild(uuid_input)
    captcha_div.appendChild( document.createElement("br"))
    captcha_div.appendChild(iframe)

    iframe.onload = resizeIframe
    setInterval(resizeIframe, 500);

 };

window.addEventListener('captcha_uuid', function(e) {
    uuid_input = document.getElementById("uuid_input");
    uuid_input.value = e.detail.uuid
}, false);

 
