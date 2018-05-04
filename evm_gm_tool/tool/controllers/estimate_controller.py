from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.admin import User
from tool.models import Project as ProjectModel, ProjectMember, GroupAccess
from tool.forms import UserCreateForm, UserEditForm, ProjectCreationForm, ProjectEditForm
from tool.utilies import *
import xlrd, json
import numpy as np
from scipy import optimize 
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import math

class Funcs: 
    def count_number_project_status_point(pd, project_status):
        for i in range(len(project_status)):
            if project_status[i]['AT'] == pd:
                return i+1
        return len(project_status)

    def get_index_of_evaluation(project_status, number_project_status_point, evaluation_point):
        for i in range(number_project_status_point):
            if project_status[i]['AT'] >= evaluation_point:
                return i - 1
                break
        return number_project_status_point - 1

    def init(X, Y , pd, budget, project_status, evaluation_index, number_project_status_point):
        for i in range(number_project_status_point):
            X[i] = project_status[i]['AT']/(pd*1.0)            
            if i > evaluation_index:
                project_status[i]['EV'] = project_status[i]['PV']
                project_status[i]['AC'] = project_status[i]['PV']
            Y[i] = project_status[i]['AC']/(budget*1.0)
                    
    # for gomperzt
    def gomperzt_func(parameters,xdata):
        a = parameters[0]
        b = parameters[1]
        y = parameters[2]
        return a * np.exp(-np.exp(b - y*xdata))

    # for logistic
    def logistic_func(parameters,xdata):
        a = parameters[0]
        b = parameters[1]
        y = parameters[2]
        return a / (1 + np.exp(b - y*xdata))

    # for logistic
    def bass_func(parameters,xdata):
        a = parameters[0]
        b = parameters[1]
        y = parameters[2]
        return a * ( ( 1 - np.exp(-(b + y)*xdata) ) / ( ( 1 + (y / b)*np.exp(-(b + y)*xdata) ) ) )

    # for logistic
    def weibull_func(parameters,xdata):
        a = parameters[0]
        b = parameters[1]
        y = parameters[2]
        return a * (1 - np.exp( -( xdata / y )**b ))

    #log-logistic
    def log_logistic_func(parameters,xdata):
        a = parameters[0]
        b = parameters[1]
        return ( (xdata/a)**b ) / ( 1 + (xdata/a)**b )        

    #Compute residuals of y_predicted - y_observed    
    def residuals(parameters,x_data,y_observed,func):    
        return func(parameters,x_data) - y_observed

    def getES(project_status, evaluation_index):
        # example: evaluationPoint = 9 -> current EV is: EV[8]. i = 0..8
        EV = project_status[evaluation_index]['EV']

        t = [ n for n,item in enumerate(project_status) if item['PV']>EV ][0] - 1
        return round(project_status[t]['AT'] + (EV - project_status[t]['PV'])/(project_status[t+1]['PV'] - project_status[t]['PV']), 2)
    
    def getSPI(project_status, evaluation_index):
        return round(project_status[evaluation_index]['EV']/project_status[evaluation_index]['PV'], 2) 

    def getCPI(project_status, evaluation_index):
        return round(project_status[evaluation_index]['EV']/project_status[evaluation_index]['AC'], 2)

    def getSPIt(project_status, evaluation_index):
        ES = Funcs.getES(project_status, evaluation_index)
        return round(ES/project_status[evaluation_index]['AT'], 2)
    
    def getSCI(SPI, CPI):
        return round(SPI*CPI, 2)
    
    def getSCIt(SPIt, CPI):
        return round(SPIt*CPI, 2)
    
    def getED(project_status, SPI, evaluation_index):
        return round(project_status[evaluation_index]['AT']*SPI, 2)

    def getSV(project_status, evaluation_index):
        return project_status[evaluation_index]['EV'] - project_status[evaluation_index]['PV']

    def getTV(BAC, PD, project_status, evaluation_index):
        PVrate = BAC/PD
        SV = Funcs.getSV(project_status, evaluation_index)
        return round(SV/PVrate, 2)

    def getEACtPV1(PD, TV):
        return PD - TV
    
    def getEACtPV2(PD, SPI):
        return round(PD/SPI, 2)

    def getEACtPV3(PD, SCI):
        return round(PD/SCI, 2)   

    # return EACt caculated by ED
    def getEACtED(PD, project_status, ED, PF, evaluation_index):
        return round(project_status[evaluation_index]['AT'] + (max(PD, project_status[evaluation_index]['AT']) - ED)/PF, 2)

     # return EACt caculated by ES
    def getEACtES(PD, project_status, ES, PF, evaluation_index):
        return round(project_status[evaluation_index]['AT'] + (PD - ES)/PF, 2)

    def getCI(CPI, w_cpi, SPI, w_spi):
        return CPI*w_cpi + SPI*w_spi

    def getCIt(CPI, w_cpi, SPIt, w_spit):
        return CPI*w_cpi + SPIt*w_spit

    # EAC caculated by EVM
    def getEAC(project_status, BAC, evaluation_index, PF):
        return round(project_status[evaluation_index]['AC'] + (BAC - project_status[evaluation_index]['EV'])/PF, 2)
    
    def getEACGM(project_status, xdata, evaluation_index, growModel, parametersEstimated, BAC, index = 1.0):
        if(growModel == 'gompertz'):
            restBudget = (Funcs.gomperzt_func(parametersEstimated, index) - Funcs.gomperzt_func(parametersEstimated, xdata[evaluation_index]))*BAC
        elif(growModel == 'logistic'):
            restBudget = (Funcs.logistic_func(parametersEstimated, index) - Funcs.logistic_func(parametersEstimated, xdata[evaluation_index]))*BAC
        elif(growModel == 'bass'):
            restBudget = (Funcs.bass_func(parametersEstimated, index) - Funcs.bass_func(parametersEstimated, xdata[evaluation_index]))*BAC
        elif(growModel == 'weibull'):
            restBudget = (Funcs.weibull_func(parametersEstimated, index) - Funcs.weibull_func(parametersEstimated, xdata[evaluation_index]))*BAC                        
        else:
            restBudget = (Funcs.log_logistic_func(parametersEstimated, index) - Funcs.log_logistic_func(parametersEstimated, xdata[evaluation_index]))*BAC
            
        
        return round(project_status[evaluation_index]['AC'] + restBudget, 2)

    def optimizeLeastSquares(growModel, xdata, ydata, method = 'trf'):
        x0 = [0.1, 0.2, 0.3] 
        if(growModel == 'gompertz'):
            OptimizeResult  = optimize.least_squares(Funcs.residuals,  x0,method = method,
                                          args   = ( xdata, ydata,Funcs.gomperzt_func) )
        elif(growModel == 'logistic'):
            OptimizeResult  = optimize.least_squares(Funcs.residuals,  x0,method = method,
                                          args   = ( xdata, ydata,Funcs.logistic_func) )
        elif(growModel == 'bass'):
            OptimizeResult  = optimize.least_squares(Funcs.residuals,  x0,method = method,
                                          args   = ( xdata, ydata,Funcs.bass_func) )
        elif(growModel == 'log_logistic'):
            x0 = [0.1, 0.2]
            OptimizeResult  = optimize.least_squares(Funcs.residuals,  x0,method = method,
                                          args   = ( xdata, ydata,Funcs.log_logistic_func) )
        else:
            OptimizeResult  = optimize.least_squares(Funcs.residuals,  x0,method = method,
                                          args   = ( xdata, ydata,Funcs.weibull_func) )

        parametersEstimated = OptimizeResult.x
        return parametersEstimated

    def estimate(project_id, grow_model, evaluation_point, algorithm="trf"):
        project = get_or_none(ProjectModel, pk=project_id)
        if project is None:
            return {}
        pd = project.pd
        budget = project.budget
        project_status = json.loads(project.status)        
        number_project_status_point = Funcs.count_number_project_status_point(pd, project_status)
        
        xdata = np.zeros(number_project_status_point)
        ydata = np.zeros(number_project_status_point)
        evaluation_index = Funcs.get_index_of_evaluation(project_status, number_project_status_point, evaluation_point)        
        Funcs.init(xdata, ydata, pd, budget, project_status, evaluation_index, number_project_status_point)                 

        ES = Funcs.getES(project_status, evaluation_index)
        SPI = Funcs.getSPI(project_status, evaluation_index)
        CPI = Funcs.getCPI(project_status, evaluation_index)
        SPIt = Funcs.getSPIt(project_status, evaluation_index)
        SCI = Funcs.getSCI(SPI, CPI)
        SCIt = Funcs.getSCIt(SPIt, CPI)
        TV = Funcs.getTV(budget, pd, project_status, evaluation_index)
        ED = Funcs.getED(project_status, SPI, evaluation_index)
        EACtPV1 = Funcs.getEACtPV1(pd, Funcs.getTV(budget, pd, project_status, evaluation_index))
        EACtPV2 = Funcs.getEACtPV2(pd, SPI)
        EACtPV3 = Funcs.getEACtPV3(pd, SCI)        

        EACtED1 = Funcs.getEACtED(pd, project_status, ED, 1, evaluation_index)
        EACtED2 = Funcs.getEACtED(pd, project_status, ED, SPI, evaluation_index)
        EACtED3 = Funcs.getEACtED(pd, project_status, ED, SCI, evaluation_index)
        
        EACtES1 = Funcs.getEACtES(pd, project_status, ES, 1, evaluation_index)
        EACtES2 = Funcs.getEACtES(pd, project_status, ES, SPIt, evaluation_index)
        EACtES3 = Funcs.getEACtES(pd, project_status, ES, SCIt, evaluation_index)
        
        EAC1 = Funcs.getEAC(project_status, budget, evaluation_index, 1)
        EAC2 = Funcs.getEAC(project_status, budget, evaluation_index, CPI)
        EAC3 = Funcs.getEAC(project_status, budget, evaluation_index, SPI)
        EAC3_SPI = Funcs.getEAC(project_status, budget, evaluation_index, SPI)
        EAC3_SPIt = Funcs.getEAC(project_status, budget, evaluation_index, SPIt)
        EAC4_SCI = Funcs.getEAC(project_status, budget, evaluation_index, SCI)
        EAC4_SCIt = Funcs.getEAC(project_status, budget, evaluation_index, SCIt)
        
        CI = Funcs.getCI(CPI, 0.8, SPI, 0.2)
        CIt = Funcs.getCIt(CPI, 0.8, SPIt, 0.2)
        EAC5_CI = Funcs.getEAC(project_status, budget, evaluation_index, CI)
        EAC5_CIt = Funcs.getEAC(project_status, budget, evaluation_index, CIt)
        parametersEstimated = Funcs.optimizeLeastSquares(grow_model, xdata, ydata, method=algorithm)
        EAC_GM1 = Funcs.getEACGM(project_status, xdata, evaluation_index, grow_model, parametersEstimated, budget, 1.0)
        EAC_GM2 = Funcs.getEACGM(project_status, xdata, evaluation_index, grow_model, parametersEstimated, budget, 1.0/SPIt)
        #caculate EAC GM3 by EAC4_SCIt
        EAC_GM3 = Funcs.getEACGM(project_status, xdata, evaluation_index, grow_model, parametersEstimated, budget, EACtES3/pd)
        #caculate EAC GM3 by EAC4_1        
        EAC_GM4 = Funcs.getEACGM(project_status, xdata, evaluation_index, grow_model, parametersEstimated, budget, EACtES1/pd)
        

        alpha = round(parametersEstimated[0], 6)
        beta = round(parametersEstimated[1], 6)
        if(grow_model == 'log_logistic'):
            gamma = ''
        else:
            gamma = round(parametersEstimated[2], 6)

        data = {
            'alpha': alpha,
            'beta': beta,
            'gamma': gamma,
            'ES': ES,
            'SPI': SPI,
            'CPI': CPI, 
            'SPIt': SPIt,
            'SCI': SCI,
            'SCIt': SCIt, 
            'TV': TV, 
            'ED': ED,
            'EACtPV1': EACtPV1,
            'EACtPV2': EACtPV2,
            'EACtPV3': EACtPV3,
            'EACtED1': EACtED1,
            'EACtED2': EACtED2,
            'EACtED3': EACtED3,
            'EACtES1': EACtES1,
            'EACtES2': EACtES2,
            'EACtES3': EACtES3,
            'EAC1': EAC1,
            'EAC2': EAC2,
            'EAC3_SPI': EAC3_SPI,
            'EAC3_SPIt': EAC3_SPIt,
            'EAC4_SCI': EAC4_SCI,
            'EAC4_SCIt': EAC4_SCIt,
            'EAC5_CI': EAC5_CI,
            'EAC5_CIt': EAC5_CIt,
            'EAC_GM1': EAC_GM1,
            'EAC_GM2': EAC_GM2,
            'EAC_GM3': EAC_GM3,
            'EAC_GM4': EAC_GM4
        }
        return data
    
    def get_pe(project_id, grow_model, evaluation_point):
        project = get_or_none(ProjectModel, pk=project_id)
        if project is None:
            return {}
        project_ac = project.get_ac()
        estimate_data = Funcs.estimate(project_id, grow_model, evaluation_point)
        data = {}
        data['pe_EAC1'] = round((estimate_data['EAC1'] - project_ac)*100/project_ac, 2)
        data['pe_EAC2'] = round((estimate_data['EAC2'] - project_ac)*100/project_ac, 2)
        data['pe_EAC3_SPI'] = round((estimate_data['EAC3_SPI'] - project_ac)*100/project_ac, 2)
        data['pe_EAC3_SPIt'] = round((estimate_data['EAC3_SPIt'] - project_ac)*100/project_ac, 2)
        data['pe_EAC4_SCI'] = round((estimate_data['EAC4_SCI'] - project_ac)*100/project_ac, 2)
        data['pe_EAC4_SCIt'] = round((estimate_data['EAC4_SCIt'] - project_ac)*100/project_ac, 2)
        data['pe_EAC5_CI'] = round((estimate_data['EAC5_CI'] - project_ac)*100/project_ac, 2)
        data['pe_EAC5_CIt'] = round((estimate_data['EAC5_CIt'] - project_ac)*100/project_ac, 2)
        data['pe_EAC_GM1'] = round((estimate_data['EAC_GM1'] - project_ac)*100/project_ac, 2)
        data['pe_EAC_GM2'] = round((estimate_data['EAC_GM2'] - project_ac)*100/project_ac, 2)
        data['pe_EAC_GM3'] = round((estimate_data['EAC_GM3'] - project_ac)*100/project_ac, 2)
        data['pe_EAC_GM4'] = round((estimate_data['EAC_GM4'] - project_ac)*100/project_ac, 2)
        return data
    
    def get_mape(project_ids, grow_model, evaluation_percent):
        projects = ProjectModel.objects.filter(pk__in=project_ids)
        data_mape = {}
        data_pe = {}
        for project in projects:
            evaluation_point = math.ceil(project.pd*evaluation_percent)
            data_pe['{}'.format(project.id)] = Funcs.get_pe(project.id, grow_model, evaluation_point)
        sum_pe = [0,0,0,0,0,0,0,0,0,0,0,0]
        for project_id in project_ids:
            sum_pe[0] += abs(data_pe['{}'.format(project_id)]['pe_EAC1'])
            sum_pe[1] += abs(data_pe['{}'.format(project_id)]['pe_EAC2'])
            sum_pe[2] += abs(data_pe['{}'.format(project_id)]['pe_EAC3_SPI'])
            sum_pe[3] += abs(data_pe['{}'.format(project_id)]['pe_EAC3_SPIt'])
            sum_pe[4] += abs(data_pe['{}'.format(project_id)]['pe_EAC4_SCI'])
            sum_pe[5] += abs(data_pe['{}'.format(project_id)]['pe_EAC4_SCIt'])
            sum_pe[6] += abs(data_pe['{}'.format(project_id)]['pe_EAC5_CI'])
            sum_pe[7] += abs(data_pe['{}'.format(project_id)]['pe_EAC5_CIt'])
            sum_pe[8] += abs(data_pe['{}'.format(project_id)]['pe_EAC_GM1'])
            sum_pe[9] += abs(data_pe['{}'.format(project_id)]['pe_EAC_GM2'])
            sum_pe[10] += abs(data_pe['{}'.format(project_id)]['pe_EAC_GM3'])
            sum_pe[11] += abs(data_pe['{}'.format(project_id)]['pe_EAC_GM4'])
        return {
            'mape_EAC1': round(sum_pe[0]/len(project_ids), 2),
            'mape_EAC2': round(sum_pe[1]/len(project_ids), 2),
            'mape_EAC3_SPI': round(sum_pe[2]/len(project_ids), 2),
            'mape_EAC3_SPIt': round(sum_pe[3]/len(project_ids), 2),
            'mape_EAC4_SCI': round(sum_pe[4]/len(project_ids), 2),
            'mape_EAC4_SCIt': round(sum_pe[5]/len(project_ids), 2),
            'mape_EAC5_CI': round(sum_pe[6]/len(project_ids), 2),
            'mape_EAC5_CIt': round(sum_pe[7]/len(project_ids), 2),
            'mape_EAC_GM1': round(sum_pe[8]/len(project_ids), 2),
            'mape_EAC_GM2': round(sum_pe[9]/len(project_ids), 2),
            'mape_EAC_GM3': round(sum_pe[10]/len(project_ids), 2),
            'mape_EAC_GM4': round(sum_pe[11]/len(project_ids), 2)
        }

class MyIO:
    
    def writeResultToFile(project_name, grow_model, evaluation_time, data):
        static_dir = settings.STATICFILES_DIRS[0]

        #Creating a folder in static directory
        new_pro_dir_path = os.path.join(static_dir,'%s'%(project_name))
        new_pro_gro_dir_path = os.path.join(static_dir,'%s/%s'%(project_name, grow_model))
        new_pro_gro_eva_dir_path = os.path.join(static_dir, '%s/%s/%s'%(project_name, grow_model, evaluation_time))
        result_file_path = os.path.join(static_dir, '%s/%s/%s/data.json'%(project_name, grow_model, evaluation_time))

        if not os.path.exists(new_pro_dir_path):
            os.makedirs(new_pro_dir_path)

        if not os.path.exists(new_pro_gro_dir_path):
            os.makedirs(new_pro_gro_dir_path)
        
        if not os.path.exists(new_pro_gro_eva_dir_path):
            os.makedirs(new_pro_gro_eva_dir_path)
        
        with open(result_file_path, 'w') as f:
            json.dump(data, f)

class EstimateController:   
    def index(request):
        projects = ProjectModel.get_projects_has_access(request.user.id)
        return render(request, 'tool/estimate/index.html', {'projects': projects})

    def estimate(request):
        project_id = int(request.GET.get('project_id'))
        grow_model = request.GET.get('grow_model')
        evaluation_point = int(request.GET.get('evaluation_point'))
        algorithm = request.GET.get('algorithm')
        data = Funcs.estimate(project_id, grow_model, evaluation_point, algorithm)
        return JsonResponse({'status': 200, 'data': data})

class PeController:
    def get_pe(request):
        project_id = request.GET.get('project_id')
        project = get_or_none(ProjectModel, pk=project_id)
        project_ac = project.get_ac()
        evaluation_percents = [0.25, 0.5, 0.75]
        grow_models = ['gompertz', 'logistic', 'bass', 'weibull']
        # grow_models = ['gompertz', 'logistic', 'weibull', 'bass', 'log_logistic']        
        data = {}
        for grow_model in grow_models:    
            data['{}'.format(grow_model)] = {}                    
            for evaluation_percent in evaluation_percents:
                evaluation_point = math.ceil(project.pd*evaluation_percent)
                data['{}'.format(grow_model)]['{}'.format(evaluation_percent)] = Funcs.get_pe(project_id, grow_model, evaluation_point)
        return JsonResponse({'data': data})
    
    def get_mape(request):
        project_ids_str = request.GET.get('project_ids')
        project_ids = json.loads(project_ids_str)
        evaluation_percents = [0.25, 0.5, 0.75]
        grow_models = ['gompertz', 'logistic', 'weibull', 'bass']
        # grow_models = ['gompertz', 'logistic', 'weibull', 'bass', 'log_logistic']
        data = {}
        for grow_model in grow_models:    
            data['{}'.format(grow_model)] = {}                    
            for evaluation_percent in evaluation_percents:
                data['{}'.format(grow_model)]['{}'.format(evaluation_percent)] = Funcs.get_mape(project_ids, grow_model, evaluation_percent)
        return JsonResponse({'data': data})
        