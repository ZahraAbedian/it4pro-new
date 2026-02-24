document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById('saveAndNext').addEventListener('click',function(event){
        event.preventDefault();
        qForm = document.getElementById('qForm')
        var myVarMcod = parseInt(document.getElementById("myVarMcod").value)
        var myVar = parseInt(document.getElementById("myVarCCO").value)
        var myVarnew = parseInt(document.getElementById("myVarCCO").value)+1;
        qForm.action = "/questions/?cod="+myVarnew+"&pcod="+myVar+"&mcod="+myVarMcod
        qForm.submit()
    },false);

    document.getElementById('saveAndPrevious').addEventListener('click',function(event){
        event.preventDefault();
        qForm = document.getElementById('qForm')
        var myVarMcod = parseInt(document.getElementById("myVarMcod").value)
        var myVar = parseInt(document.getElementById("myVarCCO").value)
        var myVarnew = parseInt(document.getElementById("myVarCCO").value)-1;
        qForm.action = "/questions/?cod="+myVarnew+"&pcod="+myVar+"&mcod="+myVarMcod
        qForm.submit()
    },false);

    // var categoriesItems = document.getElementsByClassName("categoriesListsItems");
    // for (var i = 0; i < categoriesItems.length; i++) {
    //     categoriesItems.item(i).addEventListener('click', function(e){
    //     for (var j = 0; j < categoriesItems.length; j++) {
    //         categoriesItems.item(j).classList.remove("categoryActive");
    //     }
    //     this.classList.add("categoryActive");
    //     });
    // }

});

