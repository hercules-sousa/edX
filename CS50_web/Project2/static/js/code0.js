document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("#div_form").style.visibility = "hidden"
    if(!localStorage.getItem("user")){
        document.querySelector("#div_form").style.visibility = "visible"
    }
})