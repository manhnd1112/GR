$(document).ready(function(){
    var project_status = []

    function create_line_chart(ctx, data=[]) {
        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    function update_chart(chart, project_status_data){
        var data = {
            labels: project_status_data['AT'],
            datasets: [{
                label: "PV",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "orange",
                borderColor: "orange", // The main line color
                borderCapStyle: 'square',
                borderDash: [], // try [5, 15] for instance
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "black",
                pointBackgroundColor: "white",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderColor: "brown",
                pointHoverBorderWidth: 2,
                pointRadius: 4,
                pointHitRadius: 10,
                // notice the gap in the data and the spanGaps: true
                data: project_status_data['PV'],
                spanGaps: true,
              },
              {
                label: "EV",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "green",
                borderColor: "green", // The main line color
                borderCapStyle: 'square',
                borderDash: [], // try [5, 15] for instance
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "black",
                pointBackgroundColor: "white",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderColor: "brown",
                pointHoverBorderWidth: 2,
                pointRadius: 4,
                pointHitRadius: 10,
                // notice the gap in the data and the spanGaps: true
                data: project_status_data['EV'],
                spanGaps: true,
              },
              {
                label: "AC",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "red",
                borderColor: "red", // The main line color
                borderCapStyle: 'square',
                borderDash: [], // try [5, 15] for instance
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "black",
                pointBackgroundColor: "white",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderColor: "brown",
                pointHoverBorderWidth: 2,
                pointRadius: 4,
                pointHitRadius: 10,
                // notice the gap in the data and the spanGaps: true
                data: project_status_data['AC'],
                spanGaps: true,
              }
            ]
        };
        chart.config.data = data
        chart.update()
    }

    var ctx = document.getElementById("chart-pv-ev-ac").getContext('2d'); 
    var line_chart = create_line_chart(ctx)
    function get_project_detail(){
        var selected_project_id = $('.project-select-box option:selected').val()
        $.ajax({
            type: 'GET',
            url: '/ajax/get_project_detail',
            data: {
                'project_id': selected_project_id
            },
            success: function(res) {   
                if(res.status == 200) {
                    $('#pd').val(res.data.pd)
                    $('#budget').val(res.data.budget)
                    var selected_percent = $('input[name=project_evaluate]:checked').val()
                    $('#evaluation-point').val(Math.ceil(res.data.pd*selected_percent))
                    var  project_status_str = res.data.status.replace(/'/g, '"')
                    if(project_status_str != '' && project_status_str != undefined) {
                        project_status = []
                        project_status = $.parseJSON(project_status_str)
                        $('.table-project-status').find('tbody tr:not(.status-tr-template)').remove()
                        for(i = 0; i < project_status.length; i++) {
                            var status_tr_template_clone = $('.status-tr-template').clone().removeClass("status-tr-template")
                            status_tr_template_clone.css('display', 'table-row')
                            status_tr_template_clone.find('.AT').html(project_status[i]["AT"])
                            status_tr_template_clone.find('.PV').html(project_status[i]["PV"])
                            status_tr_template_clone.find('.EV').html(project_status[i]["EV"])
                            status_tr_template_clone.find('.AC').html(project_status[i]["AC"])
                            $('.table-project-status').find('tbody').append($(status_tr_template_clone))
                        }
                        line_chart_data = {};
                        line_chart_data['AT'] = $.map(project_status, function(element, index){
                            return project_status[index]['AT']
                        })
                        line_chart_data['PV'] = $.map(project_status, function(element, index){
                            return project_status[index]['PV']
                        })
                        line_chart_data['EV'] = $.map(project_status, function(element, index){
                            return project_status[index]['EV']
                        })
                        line_chart_data['AC'] = $.map(project_status, function(element, index){
                            return project_status[index]['AC']
                        })
                        update_chart(line_chart, line_chart_data)
                    }
                }
            }
        })
    }

    get_project_detail()   
     
    $('.project-select-box').change(function(){
        get_project_detail()
    })

    $('input[name=project_evaluate]').change(function(){
        var pd = $('#pd').val()
        var selected_percent = $(this).val()
        $('#evaluation-point').val(Math.ceil(pd*selected_percent))
    })

    $('#btn-est-param').click(function(){
        var pd = $('#pd').val()
        var budget = $('#budget').val()
        var evaluation_point = $('#evaluation-point').val()
        var grow_model = $('input[name=grow-model]:checked').val()
        var algorithm = $('input[name=algorithm]:checked').val()
        var selected_project_id = $('.project-select-box option:selected').val()
        console.log(algorithm)
        $.ajax({
            type: 'GET',
            url: '/estimate/estimate',
            data: {
                'project_id': selected_project_id,
                'evaluation_point': evaluation_point,
                'grow_model': grow_model,
                'algorithm': algorithm
            },
            success: function(res) {   
                if(res.status = 200) {
                    $('#alpha').val(res.data.alpha)
                    $('#beta').val(res.data.beta)
                    $('#gamma').val(res.data.gamma)     
                    $('#ES').text(res.data.ES)
                    $('#SPI').text(res.data.SPI)       
                    $('#CPI').text(res.data.CPI)       
                    $('#SPIt').text(res.data.SPIt)       
                    $('#SCI').text(res.data.SCI)       
                    $('#SCIt').text(res.data.SCIt)       
                    $('#TV').text(res.data.TV)       
                    $('#ED').text(res.data.ED)       
                    $('#EACtPV1').text(res.data.EACtPV1)
                    $('#EACtPV2').text(res.data.EACtPV2)
                    $('#EACtPV3').text(res.data.EACtPV3)
                    $('#EACtED1').text(res.data.EACtED1)            
                    $('#EACtED2').text(res.data.EACtED2)            
                    $('#EACtED3').text(res.data.EACtED3)
                    $('#EACtES1').text(res.data.EACtES1)                        
                    $('#EACtES2').text(res.data.EACtES2)                        
                    $('#EACtES3').text(res.data.EACtES3)
                    $('#EAC1').text(res.data.EAC1)                                                
                    $('#EAC2').text(res.data.EAC2)                                                
                    $('#EAC3-SPI').text(res.data.EAC3_SPI)                                                
                    $('#EAC3-SPIt').text(res.data.EAC3_SPIt)    
                    $('#EAC4-SCI').text(res.data.EAC4_SCI)                                                            
                    $('#EAC4-SCIt').text(res.data.EAC4_SCIt)
                    $('#EAC5-CI').text(res.data.EAC5_CI)                                                            
                    $('#EAC5-CIt').text(res.data.EAC5_CIt)                                                                        
                    $('#EAC-GM1').text(res.data.EAC_GM1)                                                                        
                    $('#EAC-GM2').text(res.data.EAC_GM2)
                    $('#EAC-GM3').text(res.data.EAC_GM3)
                    $('#EAC-GM4').text(res.data.EAC_GM4)
                } else {
                    alert(res.err)
                }
            }
        })
    })

    function export_xlsx() {
        var opts = [{sheetid:'Sheet One',header:true}];
        var result = alasql('SELECT * INTO XLSX("'+this.keyword+'_page_from'+this.pageStart+"-"+this.pageEnd+'_favorite_'+this.lowestFavoriteNumber+'.xlsx",?) FROM ?',
                          [opts,[this.data]]);
    }
})