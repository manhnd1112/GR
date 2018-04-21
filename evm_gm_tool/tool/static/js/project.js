$(document).ready(function(){
    var BASE_SERVER_IP = 'http://127.0.0.1:8000'
    
    var total_status_field = 0;
    var project_status = [];
    var cleaned_project_status = [];

    var total_member_field = 0;
    var project_members = [];
    var cleaned_project_members = [];

    var project_status_field = $('.project-status-field');
    
    var search_result_member_item_field = $('.search-result-member-item-field');
    var member_item_field = $('.member-item-field');

    $("table.project-list").stupidtable();    

    gennerate_project_status_html();
    gennerate_project_member_html();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $('.icon-delete').click(function(){
        return confirm("Are you sure you want to delete this project?")
    })
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            console.log(csrftoken);
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.btn-add-project-status').click(function(){
        total_status_field++;        

        project_status_field_clone = $(project_status_field).clone();
        project_status_field_clone.attr('index', total_status_field);
        project_status_field_clone.css('display', 'block');    
        add_status_field_listen_change(project_status_field_clone);
    
        $('.project-status').append($(project_status_field_clone));
    })



    $('.btn-import-project-status-from-csv').click(function(){
        var input_file = $(this).closest('form').find('input.file-input-data');
        if(input_file.length != 0) {
            if(confirm('All current project status will be deleted if you load data from csv file.\nAre you sure?')) {
                input_file.click();        
            }
        }
    });


    $('input.file-input-data').change(function(){
        if($(this).prop('files') != undefined) {
            var file = $(this).prop('files')[0];
            var form_data = new FormData();
            form_data.append('file', file)
            $.ajax({
                type: 'POST',
                url: '/common/upload_csv',
                data: form_data,
                contentType: false, 
                processData: false,
                success: function(res) {          
                    remove_all_project_status();
                    var AT_data = res.data[0];
                    var PV_data = res.data[1];
                    var EV_data = res.data[2];
                    var AC_data = res.data[3];
                    total_status_field = AT_data.length > 0? AT_data.length: 0;
                    var pd = -1;
                    var budget = PV_data[PV_data.length-1] 
                    for(let index= 0; index < AT_data.length; index++){
                        project_status[index] = {};
                        project_status[index]["AT"] = AT_data[index]
                        project_status[index]["PV"] = PV_data[index]
                        project_status[index]["EV"] = EV_data[index]
                        project_status[index]["AC"] = AC_data[index]
                        var project_status_field_clone = create_new_project_status_field_clone(
                            index,
                            project_status[index]["AT"],
                            project_status[index]["PV"],
                            project_status[index]["EV"],
                            project_status[index]["AC"]
                        )
                        add_status_field_listen_change(project_status_field_clone);        
                        $('.project-status').append($(project_status_field_clone));
                        
                        if(PV_data[index] == budget && pd == -1) pd = AT_data[index]
                    }
                    $('input[name=budget]').val(budget)
                    $('input[name=pd]').val(pd)
                    clean_project_status();
                }
            })
        }
    })

    function remove_all_project_status() {
        $('.project-status').empty();
        total_status_field = 0;
        project_status = [];
    }

    function add_status_field_listen_change(element){
        $(element).find('.AT').change(function(){
            update_project_status(element);
        })
        $(element).find('.PV').change(function(){
            update_project_status(element);
        })
        $(element).find('.EV').change(function(){
            update_project_status(element);
        })
        $(element).find('.AC').change(function(){
            update_project_status(element);
        })
        $(element).find('.btn-remove').click(function(){
            if(confirm('Are you sure delete this data?')) {
                remove_project_status_field(element);            
            }
        })
    }
    
    function project_status_field_is_null(project_status_field){
        if(project_status_field == undefined) return true;
        return(project_status_field['AT'] === '' 
            && project_status_field['PV'] === ''
            && project_status_field['EV'] === ''
            && project_status_field['AC'] === ''
        )
    }

    function clean_project_status(){
        cleaned_project_status= [];
        var i = 0;
        $.each(project_status, function(index){
            if(!project_status_field_is_null(project_status[index])) {
                cleaned_project_status[i++] = project_status[index];
            }
        })
        console.log(cleaned_project_status);
        var json_str = JSON.stringify(cleaned_project_status);
        $('textarea[name=status]').html(json_str);
        console.log($('textarea[name=status]').html())
    }

    function update_project_status(element){
        status_field_index = $(element).attr('index');
        var status_field = {};
        status_field['AT'] = parseFloat($(element).find('.AT').val());
        status_field['PV'] = parseFloat($(element).find('.PV').val());
        status_field['EV'] = parseFloat($(element).find('.EV').val());
        status_field['AC'] = parseFloat($(element).find('.AC').val());
        project_status[status_field_index] = status_field;
        
        clean_project_status();
    }

    function remove_project_status_field(element){
        status_field_index = $(element).attr('index');        
        project_status[status_field_index] = undefined;
        $(element).remove();
        clean_project_status();        
    }


    function gennerate_project_status_html(){
        var form_project_update = $('.form.project-update-form');
        var form_project_create = $('.form.project-creation-form');
        if(form_project_update.length != 0) {
            var project_status_str = form_project_update.find('textarea[name=status]').text().replace(/'/g, '"');
            if(project_status_str != '' && project_status_str != undefined) {
                project_status = $.parseJSON(project_status_str);
                total_status_field = project_status.length > 0? project_status.length: 0;
                $.each(project_status, function(index){
                    var project_status_field_clone = $(project_status_field).clone();
                    project_status_field_clone.css('display', 'block');
                    project_status_field_clone.attr('index', index)
                    project_status_field_clone.find('.AT').val(project_status[index]["AT"])
                    project_status_field_clone.find('.PV').val(project_status[index]["PV"])
                    project_status_field_clone.find('.EV').val(project_status[index]["EV"])
                    project_status_field_clone.find('.AC').val(project_status[index]["AC"])
                    add_status_field_listen_change(project_status_field_clone);        
                    $('.project-status').append($(project_status_field_clone));
                })
                clean_project_status();
            }
        }

        if(form_project_create.length != 0) {
            var project_status_field_clone = $(project_status_field).clone();
            project_status_field_clone.attr('index', total_status_field);
            project_status_field_clone.css('display', 'block');    
            add_status_field_listen_change(project_status_field_clone);
        
            $('.project-status').append($(project_status_field_clone));
        }
    }

    function create_new_project_status_field_clone(index=0, AT='', PV= '', EV='', AC=''){
        var project_status_field_clone = $(project_status_field).clone();
        project_status_field_clone.css('display', 'block');
        project_status_field_clone.attr('index', index)
        project_status_field_clone.find('.AT').val(AT)
        project_status_field_clone.find('.PV').val(PV)
        project_status_field_clone.find('.EV').val(EV)
        project_status_field_clone.find('.AC').val(AC)
        return project_status_field_clone;
    }


    /// MEMBER
    $(document).click(function(event) { 
        if(!$(event.target).closest('.search-result').length && !$(event.target).closest('.search-member').length) {
            if($('.search-result').is(":visible")) {
                $('.search-result').hide();
            }
        }        
    });
    $('.add-project-member-area .search-member').on('keyup focus',function(){
        $('ul.search-result').css('display', 'block');
        var keyword = $(this).val();
        var id_owner = parseInt($('select#id_owner option:selected').val());
        $.ajax({
            url: '/ajax/search_user',
            type: 'GET',
            data: {
                'keyword': keyword
            },
            dataType: 'json',
            success: function(res){
                var users = res.users;
                $('.search-result').empty();
                $.each(users, function(index, user){
                    if(user['id'] != id_owner) {
                        var search_result_member_item_field_clone = search_result_member_item_field.clone();
                        search_result_member_item_field_clone.css('display', 'block');
                        search_result_member_item_field_clone.attr('user-id', user['id']);
                        search_result_member_item_field_clone.attr('avatar-url', user['avatar-url']);
                        search_result_member_item_field_clone.html(user['username']);
                        add_search_result_field_listen_click(search_result_member_item_field_clone)
                        $('.search-result').append(search_result_member_item_field_clone);
                    }
                })
            }
        })
    })

    $('.btn-add-project-member').click(function(){
        var selected_user_id = $('input.search-member').attr('selected-user-id'); 
        var selected_user_avatar_url = $('input.search-member').attr('selected-user-avatar-url'); 
        if(is_project_member_already_added(selected_user_id)) {
            alert("Member already added as project member");
        } else {
            var project_id = $('input[name=id]').val();
            var group_access = $('.select-box-group-access').val()
            var selected_username = $('input.search-member').val()
            if (selected_username == '' || selected_username == undefined){
                alert('Error. Select user to add');
                return
            }
            var form_project_update = $('.form.project-update-form');
            if(form_project_update.length != 0) {
                $.ajax({
                    url: '/ajax/add_project_member',
                    type: 'GET',
                    data: {
                        'project_id': project_id,
                        'user_id': selected_user_id,
                        'group_access': group_access
                    },
                    dataType: 'json',
                    success: function(res){
                        if(res.status == 200) {
                            add_member_field(selected_user_id, group_access, res.id, selected_user_avatar_url)
                        } else {
                            alert(res.err)
                        }
                    }
                })
            } else {
                add_member_field(selected_user_id, group_access, '', selected_user_avatar_url)
            }
            
        }
    })

    function add_member_field(selected_user_id, group_access, id='', avatar_url = ''){
        project_members[total_member_field] = {}
        project_members[total_member_field]["id"] = id
        project_members[total_member_field]["avatar-url"] = avatar_url
        project_members[total_member_field]["user-id"] = selected_user_id
        project_members[total_member_field]["username"] = $('input.search-member').val()            
        project_members[total_member_field]["group-access"] = group_access
        var member_item_field_clone = member_item_field.clone()
        member_item_field_clone.css('display', 'block')
        member_item_field_clone.attr('index', total_member_field);
        member_item_field_clone.find('.id').text(project_members[total_member_field]["id"]);
        member_item_field_clone.find('.user-image').attr('src', project_members[total_member_field]["avatar-url"]);
        member_item_field_clone.find('.user-id').text(project_members[total_member_field]["user-id"]);
        member_item_field_clone.find('.username').text(project_members[total_member_field]["username"]);
        member_item_field_clone.find('.group-access').eq(project_members[total_member_field]["group-access"]).addClass('active')
        $('.project-members').append(member_item_field_clone);
        total_member_field++;
        add_member_field_listen(member_item_field_clone);    
        clean_project_members();
    }

    function add_search_result_field_listen_click(element){
        $(element).click(function(){
            $('ul.search-result').css('display', 'none');
            $('input.search-member').val($(this).text());
            $('input.search-member').attr('selected-user-id', $(this).attr('user-id'));
            $('input.search-member').attr('selected-user-avatar-url', $(this).attr('avatar-url'));
            console.log($('input.search-member'))
        })
    }

    function add_member_field_listen(element) {
        $(element).find('.group-access').click(function(){            
            var el = $(this).closest('.member-item-field');
            var index = $(el).attr('index');
            var project_id = $('input[name=id]').val();
            var group_access = parseInt($(this).attr('group-access'));
            var project_member_id = project_members[index]["id"];
            var _this = this;
            var form_project_update = $('.form.project-update-form');
            if(form_project_update.length != 0) {
                $.ajax({
                    url: '/ajax/update_group_access',
                    type: 'GET',
                    data: {
                        'project_id': project_id,
                        'project_member_id': project_member_id,
                        'group_access': group_access
                    },
                    dataType: 'json',
                    success: function(res){
                        if(res.status == 200) {
                            update_group_access(el, _this, index, group_access)
                        } else {
                            alert(res.err)
                        }
                    }
                })
            } else {
                update_group_access(el, _this, index, group_access)
            }
            
        })

        function update_group_access(el, group_access_field, index, group_access) {
            project_members[index]["group-access"] = group_access
            clean_project_members();
            $(el).find('.group-access').removeClass('active');
            $(group_access_field).addClass('active');
        }

        $(element).find('.btn-remove-member').click(function(){
            if(confirm('Are you sure delete this member out of the project?')) {
                var project_id = $('input[name=id]').val();        
                var el = $(this).closest('.member-item-field');
                var index = $(el).attr('index');
                project_member_id = project_members[index]["id"];
                var form_project_update = $('.form.project-update-form');
                if(form_project_update.length != 0) {
                    $.ajax({
                        url: '/ajax/remove_member',
                        type: 'GET',
                        data: {
                            'project_id': project_id,
                            'project_member_id': project_member_id
                        },
                        dataType: 'json',
                        success: function(res){
                            console.log(res);
                            if(res.status == 200) {
                                remove_project_member(el, index);
                            } else {
                                alert(res.err);
                            }
                        }
                    })
                } else {
                    remove_project_member(el, index);
                }   
            }   
        })
    }

    function remove_project_member(el, index) {
        project_members[index] = undefined;
        console.log(project_members);
        $(el).remove();
        clean_project_members();
    }

    function clean_project_members(){
        cleaned_project_members= [];
        var i = 0;
        $.each(project_members, function(index){
            if(!project_member_field_is_null(project_members[index])) {
                cleaned_project_members[i++] = project_members[index];
            }
        })
        console.log(cleaned_project_members);
        var json_str = JSON.stringify(cleaned_project_members);
        $('input[name=members]').val(json_str);
    }
    
    function project_member_field_is_null(project_status_field){
        if(project_status_field == undefined) return true;
        return false;
    }

    function is_project_member_already_added(user_id){
        for(var i = 0; i < cleaned_project_members.length; i++) {
            if(cleaned_project_members[i]["user-id"] == user_id) return true;
        }  
        return false;
    }

    function gennerate_project_member_html(){
        var form_project_update = $('.form.project-update-form');
        if(form_project_update.length != 0) {
            var project_members_str = form_project_update.find('input[name=members]').val().replace(/'/g, '"');
            
            project_members = $.parseJSON(project_members_str);
            total_member_field = project_members.length > 0? project_members.length: 0;
            $.each(project_members, function(index, project_member){
                console.log(project_member);
                var member_item_field_clone = member_item_field.clone();
                member_item_field_clone.css('display', 'block');
                member_item_field_clone.attr('index', index);
                member_item_field_clone.find('.id').text(project_member["id"]);                
                member_item_field_clone.find('.user-id').text(project_member["user_id"]);
                member_item_field_clone.find('.user-image').attr('src', project_member["avatar_url"]);
                member_item_field_clone.find('.username').text(project_member["username"]);
                member_item_field_clone.find('.group-access').eq(project_member['group_access']).addClass('active')
                add_member_field_listen(member_item_field_clone);        
                $('.project-members').append($(member_item_field_clone));
            })
            clean_project_members()            
        }
    }


})
