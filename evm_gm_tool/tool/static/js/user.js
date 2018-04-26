$(document).ready(function(){
    $("table.user-list").stupidtable();    
    $('.icon-delete').click(function(event){
        return confirm("Are you sure you want to delete this? All of related project will be delete?")
    })
    $('.btn-delete-user').click(function(event){
        return confirm("Are you sure you want to delete this? All of related project will be delete?")        
    })
})