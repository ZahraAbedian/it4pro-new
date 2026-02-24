document.addEventListener("DOMContentLoaded", function(event) {
    
    var sideItems = document.getElementsByClassName("mainPageSidebarElm");
    for (var i = 0; i < sideItems.length; i++) {
        sideItems.item(i).addEventListener('click', function(e){
        for (var j = 0; j < sideItems.length; j++) {
            sideItems.item(j).classList.remove("active");
        }
        this.classList.add("active");
        });
    }

    document.getElementById('SideCategoryTask').addEventListener('click',function(event){
        document.getElementById('SideCategoryTaskList').classList.toggle("disappear");
        if(!window.location.href.includes("/tasks/")){
            window.location.href = window.location.origin + "/tasks/";
        }
    },false);

});

