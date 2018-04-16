$(document).ready(function(){
    var BASE_SERVER_IP = 'http://127.0.0.1:8000'
    var project_status = []

    var ctx = document.getElementById("myChart").getContext('2d');    
    var chart_gomperzt = new Chart(ctx, {
        type: 'bar',
        data: [],
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
    var ctx_logistic = document.getElementById("chartLogistic").getContext('2d');    
    var chart_logistic = new Chart(ctx_logistic, {
        type: 'bar',
        data: [],
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
    var ctx_weibull = document.getElementById("chartWeibull").getContext('2d');    
    var chart_weibull = new Chart(ctx_weibull, {
        type: 'bar',
        data: [],
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
    var ctx_bass = document.getElementById("chartBass").getContext('2d');    
    var chart_bass = new Chart(ctx_bass, {
        type: 'bar',
        data: [],
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });

    function get_mape(){
        var selected_project_id = $('.mape-project-select-box option:selected').val()
        if(selected_project_id == 'all'){
            project_option_fields = $('.mape-project-select-box option[value!="all"]');
            console.log(project_option_fields)
            project_ids = []
            for(i=0; i<project_option_fields.length; i++) {
                project_ids.push(parseInt($(project_option_fields[i]).val()))
            }
            console.log(project_ids)
            $.ajax({
                type: 'GET',
                url: `${BASE_SERVER_IP}/tool/pe/get_mape`,
                data: {
                    'project_ids': JSON.stringify(project_ids)
                },
                success: function(res) {   
                    console.log(res)
                    received_data = res.data;
                    data= {};
                    var grow_models = ['gompertz', 'logistic', 'weibull', 'bass']
                    for(let i = 0; i < grow_models.length; i++) {
                        let grow_model = grow_models[i]
                        grow_model_data = res.data[`${grow_model}`]
                        data[`${grow_model}`] = {}
                        data[`${grow_model}`]['pe_EAC1'] = [grow_model_data['0.25']['mape_EAC1'], grow_model_data['0.5']['mape_EAC1'], grow_model_data['0.75']['mape_EAC1']]
                        data[`${grow_model}`]['pe_EAC2'] = [grow_model_data['0.25']['mape_EAC2'], grow_model_data['0.5']['mape_EAC2'], grow_model_data['0.75']['mape_EAC2']]
                        data[`${grow_model}`]['pe_EAC3_SPI'] = [grow_model_data['0.25']['mape_EAC3_SPI'], grow_model_data['0.5']['mape_EAC3_SPI'], grow_model_data['0.75']['mape_EAC3_SPI']]
                        data[`${grow_model}`]['pe_EAC3_SPIt'] = [grow_model_data['0.25']['mape_EAC3_SPIt'], grow_model_data['0.5']['mape_EAC3_SPIt'], grow_model_data['0.75']['mape_EAC3_SPIt']]
                        data[`${grow_model}`]['pe_EAC4_SCI'] = [grow_model_data['0.25']['mape_EAC4_SCI'], grow_model_data['0.5']['mape_EAC4_SCI'], grow_model_data['0.75']['mape_EAC4_SCI']]
                        data[`${grow_model}`]['pe_EAC4_SCIt'] = [grow_model_data['0.25']['mape_EAC4_SCIt'], grow_model_data['0.5']['mape_EAC4_SCIt'], grow_model_data['0.75']['mape_EAC4_SCIt']]
                        data[`${grow_model}`]['pe_EAC5_CI'] = [grow_model_data['0.25']['mape_EAC5_CI'], grow_model_data['0.5']['mape_EAC5_CI'], grow_model_data['0.75']['mape_EAC5_CI']]
                        data[`${grow_model}`]['pe_EAC5_CIt'] = [grow_model_data['0.25']['mape_EAC5_CIt'], grow_model_data['0.5']['mape_EAC5_CIt'], grow_model_data['0.75']['mape_EAC5_CIt']]
                        data[`${grow_model}`]['pe_EAC_GM1'] = [grow_model_data['0.25']['mape_EAC_GM1'], grow_model_data['0.5']['mape_EAC_GM1'], grow_model_data['0.75']['mape_EAC_GM1']]
                        data[`${grow_model}`]['pe_EAC_GM2'] = [grow_model_data['0.25']['mape_EAC_GM2'], grow_model_data['0.5']['mape_EAC_GM2'], grow_model_data['0.75']['mape_EAC_GM2']]
                        write_chart(data, grow_model)                
                    }                    
                    console.log(data)
                }
            })
        } else {
            $.ajax({
                type: 'GET',
                url: `${BASE_SERVER_IP}/tool/pe/get_pe`,
                data: {
                    'project_id': selected_project_id
                },
                success: function(res) {   
                    console.log(res)
                    received_data = res.data;
                    data= {};
                    var grow_models = ['gompertz', 'logistic', 'weibull', 'bass']
                    for(let i = 0; i < grow_models.length; i++) {
                        let grow_model = grow_models[i]
                        grow_model_data = res.data[`${grow_model}`]                
                        data[`${grow_model}`] = {}
                        data[`${grow_model}`]['pe_EAC1'] = [grow_model_data['0.25']['pe_EAC1'], grow_model_data['0.5']['pe_EAC1'], grow_model_data['0.75']['pe_EAC1']]
                        data[`${grow_model}`]['pe_EAC2'] = [grow_model_data['0.25']['pe_EAC2'], grow_model_data['0.5']['pe_EAC2'], grow_model_data['0.75']['pe_EAC2']]
                        data[`${grow_model}`]['pe_EAC3_SPI'] = [grow_model_data['0.25']['pe_EAC3_SPI'], grow_model_data['0.5']['pe_EAC3_SPI'], grow_model_data['0.75']['pe_EAC3_SPI']]
                        data[`${grow_model}`]['pe_EAC3_SPIt'] = [grow_model_data['0.25']['pe_EAC3_SPIt'], grow_model_data['0.5']['pe_EAC3_SPIt'], grow_model_data['0.75']['pe_EAC3_SPIt']]
                        data[`${grow_model}`]['pe_EAC4_SCI'] = [grow_model_data['0.25']['pe_EAC4_SCI'], grow_model_data['0.5']['pe_EAC4_SCI'], grow_model_data['0.75']['pe_EAC4_SCI']]
                        data[`${grow_model}`]['pe_EAC4_SCIt'] = [grow_model_data['0.25']['pe_EAC4_SCIt'], grow_model_data['0.5']['pe_EAC4_SCIt'], grow_model_data['0.75']['pe_EAC4_SCIt']]
                        data[`${grow_model}`]['pe_EAC5_CI'] = [grow_model_data['0.25']['pe_EAC5_CI'], grow_model_data['0.5']['pe_EAC5_CI'], grow_model_data['0.75']['pe_EAC5_CI']]
                        data[`${grow_model}`]['pe_EAC5_CIt'] = [grow_model_data['0.25']['pe_EAC5_CIt'], grow_model_data['0.5']['pe_EAC5_CIt'], grow_model_data['0.75']['pe_EAC5_CIt']]
                        data[`${grow_model}`]['pe_EAC_GM1'] = [grow_model_data['0.25']['pe_EAC_GM1'], grow_model_data['0.5']['pe_EAC_GM1'], grow_model_data['0.75']['pe_EAC_GM1']]
                        data[`${grow_model}`]['pe_EAC_GM2'] = [grow_model_data['0.25']['pe_EAC_GM2'], grow_model_data['0.5']['pe_EAC_GM2'], grow_model_data['0.75']['pe_EAC_GM2']]
                        write_chart(data, grow_model)
                    }
                }
            })
        } 
        
    }
    get_mape()
    $('.mape-project-select-box').change(function(){
        get_mape()
    })

    

    function write_chart(pe_data, grow_model){
        console.log(pe_data[`${grow_model}`])
        data = {
            labels: ['25%', '50%', '75%'],
            datasets: [
                {
                    label: 'EAC1',
                    data: pe_data[`${grow_model}`]['pe_EAC1'],
                    backgroundColor: [
                        '#4286f4',
                        '#4286f4',
                        '#4286f4'
                    ]
                    // borderColor: [
                    //     'rgba(255,99,132,1)',
                    //     'rgba(255,99,132,1)',
                    //     'rgba(255,99,132,1)'
                    // ],
                    // borderWidth: 1
                },
                {
                    label: 'EAC2',
                    data: pe_data[`${grow_model}`]['pe_EAC2'],
                    backgroundColor: [
                        '#910000',
                        '#910000',
                        '#910000'
                    ]
                },
                {
                    label: 'EAC3_SPI',
                    data: pe_data[`${grow_model}`]['pe_EAC3_SPI'],
                    backgroundColor: [
                        '#007237',
                        '#007237',
                        '#007237'
                    ]
                },
                {
                    label: 'EAC3_SPIt',
                    data: pe_data[`${grow_model}`]['pe_EAC3_SPIt'],
                    backgroundColor: [
                        '#460260',
                        '#460260',
                        '#460260'
                    ]
                },
                {
                    label: 'EAC4_SCI',
                    data: pe_data[`${grow_model}`]['pe_EAC4_SCI'],
                    backgroundColor: [
                        '#0096e8',
                        '#0096e8',
                        '#0096e8'
                    ]
                },
                {
                    label: 'EAC4_SCIt',
                    data: pe_data[`${grow_model}`]['pe_EAC4_SCIt'],
                    backgroundColor: [
                        '#ff6100',
                        '#ff6100',
                        '#ff6100'
                    ]
                },
                {
                    label: 'EAC5_CI',
                    data: pe_data[`${grow_model}`]['pe_EAC5_CI'],
                    backgroundColor: [
                        '#a4e4fc',
                        '#a4e4fc',
                        '#a4e4fc'
                    ]
                },
                {
                    label: 'EAC5_CIt',
                    data: pe_data[`${grow_model}`]['pe_EAC5_CIt'],
                    backgroundColor: [
                        '#ffa3fa',
                        '#ffa3fa',
                        '#ffa3fa'
                    ]
                },
                {
                    label: 'EAC_GM1',
                    data: pe_data[`${grow_model}`]['pe_EAC_GM1'],
                    backgroundColor: [
                        '#0aad64',
                        '#0aad64',
                        '#0aad64'
                    ]
                },
                {
                    label: 'EAC_GM2',
                    data: pe_data[`${grow_model}`]['pe_EAC_GM2'],
                    backgroundColor: [
                        '#f3ceff',
                        '#f3ceff',
                        '#f3ceff'
                    ]
                }
            ]
        };
        if(grow_model == 'gompertz') {
            chart_gomperzt.config.data = data;
            chart_gomperzt.update();
        } else if (grow_model == 'logistic') {
            chart_logistic.config.data = data;
            chart_logistic.update();
        } else if (grow_model == 'weibull') {
            chart_weibull.config.data = data;
            chart_weibull.update();
        } else if (grow_model == 'bass') {
            chart_bass.config.data = data;
            chart_bass.update();
        }
        
    }
})