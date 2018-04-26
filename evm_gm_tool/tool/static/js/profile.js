$(document).ready(function(){
    $('#id_avatar').change(function(e){
        var reader = new FileReader();
        reader.onload = function(e) {
            $('img.avatar').attr('src', e.target.result);
        }
        reader.readAsDataURL(e.target.files[0]);
    })
    var role_list = [
        'Project Manager',        
        'QA Manager',        
        'Web Developer',
        'Team Leader',
        'Game Developer',
        'Ios Developer',
        'Android Developer',
        'Tester',
        'Product Quality Manager'
    ]
    function get_role(keyword='') {
        var results = [];
        for(let i = 0; i < role_list.length; i++) {
            if(role_list[i].toLowerCase().indexOf(keyword.toLowerCase()) != -1) {
                results.push(role_list[i])
            }
        }
        return results        
    }

    function add_event_click_role(element){
        $(element).click(function(){
            $('input.role').val($(element).text())
            $('ul.role-list').hide();
        })
    }

    $(document).click(function(event) { 
        if(!$(event.target).closest('ul.role-list').length && !$(event.target).closest('input.role').length) {
            if($('ul.role-list').is(":visible")) {
                $('ul.role-list').hide();
            }
        }        
    });

    $('input.role').on('keyup focus', function() {
        keyword = $('input.role').val();
        console.log(keyword)
        matched_role_list = get_role(keyword)
        console.log(matched_role_list)
        $('ul.role-list').empty()
        if(matched_role_list.length > 0) {
            for (let i = 0; i < matched_role_list.length; i++) {
                var role_template_clone = $('.role-template').clone().removeClass('role-template')              
                role_template_clone.text(matched_role_list[i])
                role_template_clone.css('display', 'list-item')
                $('ul.role-list').append(role_template_clone)    
                add_event_click_role(role_template_clone)
            }
            $('ul.role-list').css('display', 'block')
        }
    })
})