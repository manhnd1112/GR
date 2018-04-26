$(document).ready(function(){
    var project_status = []

    function create_bar_chart(ctx) {
        return new Chart(ctx, {
            type: 'bar',
            data: [],
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

    var ctx = document.getElementById("myChart").getContext('2d');    
    var ctx_logistic = document.getElementById("chartLogistic").getContext('2d');    
    var ctx_weibull = document.getElementById("chartWeibull").getContext('2d');    
    var ctx_bass = document.getElementById("chartBass").getContext('2d');    
    // var ctx_log_logistic = document.getElementById("chartLogLogistic").getContext('2d');    

    var chart_gomperzt = create_bar_chart(ctx)
    var chart_logistic = create_bar_chart(ctx_logistic)
    var chart_weibull = create_bar_chart(ctx_weibull)    
    var chart_bass = create_bar_chart(ctx_bass)
    // var chart_log_logistic = create_bar_chart(ctx_log_logistic)
    function round_to_two(number) {
        return Math.round(number * 100)/100
    }

    function get_mape(){
        var selected_project_id = $('.mape-project-select-box option:selected').val()
        var how_show_pe = $('input[name=how-show-pe]:checked').val()
        var grow_models = ['gompertz', 'logistic', 'weibull', 'bass']
        // var grow_models = ['gompertz', 'logistic', 'weibull', 'bass', 'log_logistic']
        var pe_eacs = ['pe_EAC1', 'pe_EAC2', 'pe_EAC3_SPI', 'pe_EAC3_SPIt', 'pe_EAC4_SCI', 'pe_EAC4_SCIt', 'pe_EAC5_CI', 'pe_EAC5_CIt', 'pe_EAC_GM1', 'pe_EAC_GM2']
        if(selected_project_id == 'all'){
            project_option_fields = $('.mape-project-select-box option[value!="all"]');
            project_ids = []
            for(i=0; i<project_option_fields.length; i++) {
                project_ids.push(parseInt($(project_option_fields[i]).val()))
            }
            $.ajax({
                type: 'GET',
                url: '/pe/get_mape',
                data: {
                    'project_ids': JSON.stringify(project_ids)
                },
                success: function(res) {   
                    received_data = res.data;
                    data= {};     

                    for(let i = 0; i < grow_models.length; i++) {
                        let grow_model = grow_models[i]
                        grow_model_data = res.data[`${grow_model}`]
                        data[`${grow_model}`] = {}
                        for(let j = 0; j < pe_eacs.length; j++) {
                            pe_eac = pe_eacs[j]
                            if(how_show_pe == 'all-time') {
                                data[`${grow_model}`][`${pe_eac}`] = [round_to_two((Math.abs(grow_model_data['0.25'][`ma${pe_eac}`])+Math.abs(grow_model_data['0.5'][`ma${pe_eac}`])+Math.abs(grow_model_data['0.75'][`ma${pe_eac}`]))/3)]                                                                            
                            } else {
                                data[`${grow_model}`][`${pe_eac}`] = [grow_model_data['0.25'][`ma${pe_eac}`],grow_model_data['0.5'][`ma${pe_eac}`],grow_model_data['0.75'][`ma${pe_eac}`]]                                                                            
                            }
                        }
                        write_chart(data, grow_model, how_show_pe)                
                    }                    
                    console.log(data)
                }
            })
        } else {
            $.ajax({
                type: 'GET',
                url: '/pe/get_pe',
                data: {
                    'project_id': selected_project_id
                },
                success: function(res) {   
                    received_data = res.data;
                    data= {};
                    var grow_models = ['gompertz', 'logistic', 'weibull', 'bass']
                    // var grow_models = ['gompertz', 'logistic', 'weibull', 'bass', 'log_logistic']
                    for(let i = 0; i < grow_models.length; i++) {
                        let grow_model = grow_models[i]
                        grow_model_data = res.data[`${grow_model}`]                
                        data[`${grow_model}`] = {}
                        for(let j = 0; j < pe_eacs.length; j++) {
                            pe_eac = pe_eacs[j]
                            if(how_show_pe == 'all-time') {
                                data[`${grow_model}`][`${pe_eac}`] = [round_to_two((Math.abs(grow_model_data['0.25'][`${pe_eac}`])+Math.abs(grow_model_data['0.5'][`${pe_eac}`])+Math.abs(grow_model_data['0.75'][`${pe_eac}`]))/3)]                                            
                            } else {
                                data[`${grow_model}`][`${pe_eac}`] = [grow_model_data['0.25'][`${pe_eac}`],grow_model_data['0.5'][`${pe_eac}`],grow_model_data['0.75'][`${pe_eac}`]]                                                                            
                            }
                        }
                        write_chart(data, grow_model, how_show_pe)  
                    }
                }
            })
        } 
        
    }
    get_mape()
    $('.mape-project-select-box').change(function(){
        get_mape()
    })

    $('input[name=how-show-pe]').change(function(){
        get_mape()
    })
    

    function write_chart(pe_data, grow_model, how_show_pe='by-phase'){
        if(how_show_pe == 'by-phase') {
            var data = {
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
                        label: 'EAC3-SPI',
                        data: pe_data[`${grow_model}`]['pe_EAC3_SPI'],
                        backgroundColor: [
                            '#007237',
                            '#007237',
                            '#007237'
                        ]
                    },
                    {
                        label: 'EAC3-SPI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC3_SPIt'],
                        backgroundColor: [
                            '#460260',
                            '#460260',
                            '#460260'
                        ]
                    },
                    {
                        label: 'EAC4-SCI',
                        data: pe_data[`${grow_model}`]['pe_EAC4_SCI'],
                        backgroundColor: [
                            '#0096e8',
                            '#0096e8',
                            '#0096e8'
                        ]
                    },
                    {
                        label: 'EAC4-SCI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC4_SCIt'],
                        backgroundColor: [
                            '#ff6100',
                            '#ff6100',
                            '#ff6100'
                        ]
                    },
                    {
                        label: 'EAC5-CI',
                        data: pe_data[`${grow_model}`]['pe_EAC5_CI'],
                        backgroundColor: [
                            '#a4e4fc',
                            '#a4e4fc',
                            '#a4e4fc'
                        ]
                    },
                    {
                        label: 'EAC5-CI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC5_CIt'],
                        backgroundColor: [
                            '#ffa3fa',
                            '#ffa3fa',
                            '#ffa3fa'
                        ]
                    },
                    {
                        label: 'EAC-GM1',
                        data: pe_data[`${grow_model}`]['pe_EAC_GM1'],
                        backgroundColor: [
                            '#0aad64',
                            '#0aad64',
                            '#0aad64'
                        ]
                    },
                    {
                        label: 'EAC-GM2',
                        data: pe_data[`${grow_model}`]['pe_EAC_GM2'],
                        backgroundColor: [
                            '#f3ceff',
                            '#f3ceff',
                            '#f3ceff'
                        ]
                    }
                ]
            };
        } else {
            var data = {
                labels: ['All Time'],
                datasets: [
                    {
                        label: 'EAC1',
                        data: pe_data[`${grow_model}`]['pe_EAC1'],
                        backgroundColor: [
                            '#4286f4'
                        ]
                    },
                    {
                        label: 'EAC2',
                        data: pe_data[`${grow_model}`]['pe_EAC2'],
                        backgroundColor: [
                            '#910000'
                        ]
                    },
                    {
                        label: 'EAC3-SPI',
                        data: pe_data[`${grow_model}`]['pe_EAC3_SPI'],
                        backgroundColor: [
                            '#007237'
                        ]
                    },
                    {
                        label: 'EAC3-SPI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC3_SPIt'],
                        backgroundColor: [
                            '#460260'
                        ]
                    },
                    {
                        label: 'EAC4-SCI',
                        data: pe_data[`${grow_model}`]['pe_EAC4_SCI'],
                        backgroundColor: [
                            '#0096e8'
                        ]
                    },
                    {
                        label: 'EAC4-SCI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC4_SCIt'],
                        backgroundColor: [
                            '#ff6100'
                        ]
                    },
                    {
                        label: 'EAC5-CI',
                        data: pe_data[`${grow_model}`]['pe_EAC5_CI'],
                        backgroundColor: [
                            '#a4e4fc'
                        ]
                    },
                    {
                        label: 'EAC5-CI(t)',
                        data: pe_data[`${grow_model}`]['pe_EAC5_CIt'],
                        backgroundColor: [
                            '#ffa3fa'
                        ]
                    },
                    {
                        label: 'EAC-GM1',
                        data: pe_data[`${grow_model}`]['pe_EAC_GM1'],
                        backgroundColor: [
                            '#0aad64'
                        ]
                    },
                    {
                        label: 'EAC-GM2',
                        data: pe_data[`${grow_model}`]['pe_EAC_GM2'],
                        backgroundColor: [
                            '#f3ceff'
                        ]
                    }
                ]
            };
        }
       
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
        // else if (grow_model == 'log_logistic') {
        //     chart_log_logistic.config.data = data;
        //     chart_log_logistic.update();
        // }
    }
})