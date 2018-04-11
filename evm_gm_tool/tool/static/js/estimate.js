$(document).ready(function(){
    var BASE_SERVER_IP = 'http://127.0.0.1:8000'
    var project_status = []
    function get_project_detail(){
        var selected_project_id = $('.project-select-box option:selected').val()
        $.ajax({
            type: 'GET',
            url: `${BASE_SERVER_IP}/tool/ajax/get_project_detail`,
            data: {
                'project_id': selected_project_id
            },
            success: function(res) {   
                if(res.status == 200) {
                    $('#pd').val(res.data.pd);
                    $('#budget').val(res.data.budget);
                    var  project_status_str = res.data.status.replace(/'/g, '"');
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
                }
            }
        })
    }

    get_project_detail();    
    $('.project-select-box').change(function(){
        get_project_detail();
    })

    $('#btn-est-param').click(function(){
        var pd = $('#pd').val();
        var budget = $('#budget').val();
        var evaluation_point = $('#evaluation-point').val();
        var grow_model = $('input[name=grow-model]:checked').val();
        $.ajax({
            type: 'GET',
            url: `${BASE_SERVER_IP}/tool/estimate/estimate`,
            data: {
                'pd':  pd,
                'budget': budget,
                'project_status': JSON.stringify(project_status),
                'evaluation_point': evaluation_point,
                'grow_model': grow_model
            },
            success: function(res) {   
                if(res.status = 200) {
                    $('#alpha').val(res.data.alpha);
                    $('#beta').val(res.data.beta);
                    $('#gamma').val(res.data.gamma);     
                    $('#ES').text(res.data.ES);
                    $('#SPI').text(res.data.SPI);       
                    $('#CPI').text(res.data.CPI);       
                    $('#SPIt').text(res.data.SPIt);       
                    $('#SCI').text(res.data.SCI);       
                    $('#SCIt').text(res.data.SCIt);       
                    $('#TV').text(res.data.TV);       
                    $('#ED').text(res.data.ED);       
                    $('#EACtPV1').text(res.data.EACtPV1);
                    $('#EACtPV2').text(res.data.EACtPV2);
                    $('#EACtPV3').text(res.data.EACtPV3);
                    $('#EACtED1').text(res.data.EACtED1);            
                    $('#EACtED2').text(res.data.EACtED2);            
                    $('#EACtED3').text(res.data.EACtED3);
                    $('#EACtES1').text(res.data.EACtES1);                        
                    $('#EACtES2').text(res.data.EACtES2);                        
                    $('#EACtES3').text(res.data.EACtES3);
                    $('#EAC1').text(res.data.EAC1);                                                
                    $('#EAC2').text(res.data.EAC2);                                                
                    $('#EAC3-SPI').text(res.data.EAC3_SPI);                                                
                    $('#EAC3-SPIt').text(res.data.EAC3_SPIt);    
                    $('#EAC4-SCI').text(res.data.EAC4_SCI);                                                            
                    $('#EAC4-SCIt').text(res.data.EAC4_SCIt);
                    $('#EAC5-CI').text(res.data.EAC5_CI);                                                            
                    $('#EAC5-CIt').text(res.data.EAC5_CIt);                                                                        
                    $('#EAC-GM1').text(res.data.EAC_GM1);                                                                        
                    $('#EAC-GM2').text(res.data.EAC_GM2);
                } else {
                    alert(res.err)
                }
            }
        })
    })
})