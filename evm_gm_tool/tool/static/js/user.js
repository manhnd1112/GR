$(document).ready(function(){
    $("table.user_list").stupidtable();    
    $('.icon-delete').click(function(event){
        return confirm("Are you sure you want to delete this? All of related project will be delete?")
    })
})