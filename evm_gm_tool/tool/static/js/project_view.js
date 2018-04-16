$(document).ready(function(){
    var  project_status_str = $('#project-status').val().replace(/'/g, '"');
    if(project_status_str != '' && project_status_str != undefined) {
        project_status = []
        project_status = $.parseJSON(project_status_str);
        $('.table-project-status').find('tbody tr:not(.status-tr-template)').remove()
        for(i = 0; i < project_status.length; i++) {
            var status_tr_template_clone = $('.status-tr-template').clone().removeClass("status-tr-template");
            status_tr_template_clone.css('display', 'table-row')
            status_tr_template_clone.find('.AT').html(project_status[i]["AT"])
            status_tr_template_clone.find('.PV').html(project_status[i]["PV"])
            status_tr_template_clone.find('.EV').html(project_status[i]["EV"])
            status_tr_template_clone.find('.AC').html(project_status[i]["AC"])
            $('.table-project-status').find('tbody').append($(status_tr_template_clone))
        }
    }
    
    $('.btn-delete-project').click(function(){
        return confirm("Are you sure you want to delete this project?")
    })
})