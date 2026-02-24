function toggleLineThrough(element){
    if(element.checked){
        element.parentElement.lastElementChild.style.textDecoration = 'line-through'
    }else{
        element.parentElement.lastElementChild.style.textDecoration = 'none'
    }
}

function showTaskDetails(element){
    // document.getElementById("ListOfTasks").value
    document.getElementById("ShowMore").innerHTML = element.lastElementChild.innerHTML;
    document.getElementById("taskDateCom").innerHTML = element.getAttribute("comDate");
    
    var taskItems = document.getElementsByClassName("taskDiv");
    for (var i = 0; i < taskItems.length; i++) {
        taskItems[i].classList.remove("activeTask");
    }
    element.classList.add("activeTask");
}

document.addEventListener("DOMContentLoaded", function(event) {
    
});