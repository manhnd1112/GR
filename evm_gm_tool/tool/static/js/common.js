$(document).ready(function(){
    $('input#search').keydown(function(event){ 
        var keyCode = (event.keyCode ? event.keyCode : event.which);   
        if (keyCode == 13) {
            var search_term = $(this).val();
            var number_record_per_page = $('input#num-record-per-page').val();
            console.log(search_term)
            console.log(window.location)
            if(search_term != '') {
                window.location = window.location.origin+window.location.pathname+'?search=' + search_term+'&per-page='+number_record_per_page;        
            } else {
                window.location = window.location.origin+window.location.pathname+'?per-page='+number_record_per_page;
            }
        }
    });

    $('input#num-record-per-page').change(function(event){ 
        var number_record_per_page = $(this).val();
        var search_term = $('input#search').val();
        console.log(window.location)
        if(search_term != '') {
            window.location = window.location.origin+window.location.pathname+'?search=' + search_term+'&per-page='+number_record_per_page;      
        } else {
            window.location = window.location.origin+window.location.pathname+'?per-page='+number_record_per_page;                  
        }
    })
})