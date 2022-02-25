from django.shortcuts import render, redirect

import datetime as dt
import datetime

from .forms import ProjForm
from .forms import CheckForm
from .forms import EmployeeInserForm
from .models import projects
from .models import employee_details
from .models import assignment
from django.http import HttpResponse
from django.core import serializers
from itertools import chain
from collections import OrderedDict
from collections import Counter
import itertools 
import json
from time import gmtime, strftime
import collections
from itertools import repeat






# INSERT Project Details

def project_form(request):

    if request.method == "GET":
        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]


        emp_projs = projects.objects.all()

        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status


            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                
            else:
                pass
        id_filter = projects.objects.filter(pk__in=new_updatestes)        
        context = {}        

        context["dataset"] = projects.objects.filter(open_status__gte='2022-02-04 13:49:16').filter(open_status__lte='2022-02-17 11:06:49')        

        
        return render(request, "employee_register/project_form.html",context)

        # reg = projects.objects.all()
        # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        # today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        # print(today_min)
        # print(today_max)
        # exit()
        # get = projects.objects.filter(open_status__gte=today_min)
        # active_projects = projects.objects.filter(open_status='2022-01-29')

        # context ={}
        # context["dataset"] = projects.objects.filter(open_status__gte='2022-02-05 09:16:57').filter(open_status__lte='2022-02-05 09:20:49')
        # return render(request, "employee_register/project_form.html",{'emp_proj':id_filter})

   
    else:

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]
        projnm = request.POST['project_name']
        platname = request.POST['option_id']
        reg = projects(project_name=projnm, platform_name=platname, open_status=split_date)
        reg.save()

        context = {}        

        context["dataset"] = projects.objects.filter(open_status__gte='2022-02-04 13:49:16').filter(open_status__lte='2022-02-17 11:06:49')

        return render(request, "employee_register/project_form.html",context)



# Employee Active and Inactive Task

def empoyee_check(request):
    if request.method == "GET":
        context ={}
        context["dataset"] = employee_details.objects.filter(status='Active')
        return render(request, "employee_register/empoyee_check.html", context)
        
    else:
        if request.method == 'POST':
            recommendations=request.POST.getlist('recommendations')
            emp_id = employee_details.objects.filter(pk__in=recommendations)

            for update_status in emp_id:
                new_status = "IN-ACTIVE"

                update_status.status = new_status
                update_status.save()

    
        # return render(request, "employee_register/check_inac.html")
        return redirect('/employee/check_inac')
         
def check_inac(request):
    context = {}
    context['dataset'] = employee_details.objects.filter(status="IN-ACTIVE")
    return render(request, "employee_register/check_inac.html",context)

           

           
# Assining task details
    
def assign_task(request):
    if request.method == "GET":

        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]


        assign = assignment.objects.values_list('employeeid', flat=True)
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
       

        date_night = dt.datetime.utcnow() + dt.timedelta(hours=10, minutes=10)
        today_night = str(date_night)
        split_night_a = today_night.split(".")
        night_today_date = split_night_a[0]

       

        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))

        emp_projs = projects.objects.all()

    
        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status

            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)

                

            else:
                pass


        id_filter = projects.objects.filter(pk__in=new_updatestes)  


        #------------------TODAY TASKS-------completee--------------- 

        assign = assignment.objects.filter(date_from__gte=today_min)

        assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min)

        asssigns_night = assignment.objects.filter(date_from__gte=night_today_date)

        proj_idds = []

        for update_s in assign_yestday:
            pro_ids = update_s.projectid
            proj_idds.append(pro_ids)

        pro_app= []

        for projs in proj_idds:
            pro_in = int(projs)
            pro_app.append(pro_in)

        empidappend = []
       
        for update_status in assign:
            empsids = update_status.employeeid
            empidappend.append(empsids)

        new_app= []
        


        for ints in empidappend:
            ints = int(ints)
            new_app.append(ints)


        

            # -------------------------------------------

        apppend_id = []
        apppend_night =[]
        active_emp_n = employee_details.objects.filter(status='Active').filter(role='IA')
        active_night = employee_details.objects.filter(status='ActiveN').filter(role='IA_Night')

       
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
        active_nighttl = employee_details.objects.filter(status='Active').filter(role='TL_Night')



        for i_d in active_emp_n:
            apppend_id.append(i_d.id)
          

        for i_d in active_night:
            apppend_night.append(i_d.id)
     

        empidssmains = []

   
        for updateee_status in asssigns_night:
            emps_ids = updateee_status.employeeid
            empidssmains.append(emps_ids)
     

        int_emp= []

        for empints in empidssmains:
            emp_in = int(empints)
            int_emp.append(emp_in) 


        new_apend_data = [] 

        difference = set(new_app).symmetric_difference(set(apppend_id))
        list_difference = list(difference)

        difference_night = set(int_emp).symmetric_difference(set(apppend_night))
        list_difference_night = list(difference_night)




        count_person_day = len(list_difference)
        count_night = len(list_difference_night)


 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)
        active_emp_night = employee_details.objects.filter(status='ActiveN').filter(pk__in=list_difference_night)
         

        return render(request, "employee_register/assign_task.html",{'active_emp':active_emp,'active_tl':active_tl,'active_nighttl':active_nighttl , 'active_night':active_emp_night  ,'emp_proj':id_filter,'date':split_daten,'count':count_person_day,'count_night':count_night})


      
    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']
            tl_id = request.POST['option_tl']

        if platname == 'none' and tl_id == 'none':
            
            return HttpResponse("TL NAME AND PROJECTS MISSINGS")
        elif platname == 'none':
            
            return HttpResponse("---------PROJECTS NAME _______MISSSING")
        elif tl_id == 'none':
            return HttpResponse("---------TL NAME _______MISSSING")
        else:
            for index, item in enumerate(recomme):
                new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                today1 = str(new_date)
                split_a = today1.split(".")
                split_date = split_a[0]
                split_date1 = str(split_date).split(" ")
                split_daten = split_date1[0]
                survey = assignment.objects.create(employeeid=item,projectid=platname,date_from=split_date,tl_id=tl_id)
            
            return render(request, "employee_register/assigned.html")



                
def reassign_task(request):
    # return HttpResponse('wrong selected')
    if request.method == "GET":
        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
     
        assign = assignment.objects.filter(date_from__gte=today_min)
        prjappend = []
        empidappend =[]



        for update_status in assign:
            
            empsids = update_status.employeeid
            empidappend.append(empsids)
            projids = update_status.projectid
            prjappend.append(projids)


            

        emp_det_id = employee_details.objects.values('id','full_name','mobile').filter(pk__in=empidappend)
        emp_projs = projects.objects.all()
        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status

            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)

            else:
                pass
    

    

                
        id_filter = projects.objects.filter(pk__in=new_updatestes)  

        #------------------TODAY TASKS-------completee--------------- 

        assign = assignment.objects.filter(from_to__gte=today_min)
             
      
        empidappend = []

        for update_status in assign:
            empsids = update_status.employeeid
            
            empidappend.append(empsids)
            

        new_app= []

       
        for ints in empidappend:
            ints = int(ints)
            new_app.append(ints)

 
            # -------------------------------------------

        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active').filter(role='IA')
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

        assign2 = assignment.objects.filter(date_from__gte=today_min)

        new_id = []

        for new_updtaes in assign2:
            emps_ids = new_updtaes.employeeid
            
            new_id.append(emps_ids)

 

        new_ints =[] 

        for intse in new_id:
            ints_d = int(intse)
            new_ints.append(ints_d)

   

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)

        new_apend_data = [] 

        difference = set(new_app).symmetric_difference(set(new_ints))
        list_difference = list(difference)
        count_person = len(list_difference)
 
 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)

 
        return render(request, "employee_register/reassign_task.html",{'emp_det':active_emp,'active_tl':active_tl ,'emp_proj':id_filter, 'date':split_daten})

    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']
            tl_id = request.POST['option_tl']

        
        if platname == 'none' and tl_id == 'none':
            
            return HttpResponse("TL NAME AND PROJECTS MISSINGS")
        elif platname == 'none':
            
            return HttpResponse("---------PROJECTS NAME _______MISSSING")
        elif tl_id == 'none':
            return HttpResponse("---------TL NAME _______MISSSING")
        else:
            for index, item in enumerate(recomme):
                new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                today1 = str(new_date)
                split_a = today1.split(".")
                split_date = split_a[0]
                split_date1 = str(split_date).split(" ")
                split_daten = split_date1[0]
                survey = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)
                update = assignment.objects.filter(employeeid= item).update(first_work_done='Done')


                
            
            return render(request, "employee_register/assigned.html")        



def assign_previous(request):
    return HttpResponse('wrong selected')
    # if request.method == "GET":

    #     new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    #     today1 = str(new_date)
    #     split_a = today1.split(".")
    #     split_date = split_a[0]
    #     split_date1 = str(split_date).split(" ")
    #     split_daten = split_date1[0]


         
    #     assign = assignment.objects.values_list('employeeid', flat=True)
        
    #     today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    #     today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    #     today = datetime.datetime.utcnow().date()

    #     yesterday = str(today - datetime.timedelta(days=1))
        

    #     srt_paqt = str(today_min)
    #     split_part = srt_paqt.split(' ')
    #     split_part[0] = yesterday
    #     yesterday_min = " ".join(map(str,split_part))
      

    #     srt_paqtmax = str(today_max)
    #     split_partmax = srt_paqtmax.split(' ')
    #     split_partmax[0] = yesterday
    #     yesterday_max = " ".join(map(str,split_partmax))
   

    #     # ---------------------todays_task----start---------------------
       
        
    #     emp_projs = projects.objects.all()

    #     new_updatestes = []

    #     for n_update in emp_projs:
    #         open_o = n_update.open_status
    #         close_o = n_update.close_status


    #         if len(open_o) != 0 and len(close_o) ==0:
    #             open_d = n_update.id
    #             new_updatestes.append(open_d)
                

    #         else:
    #             pass

    #     id_filter = projects.objects.filter(pk__in=new_updatestes)  



    #     #------------------TODAY TASKS-------completee--------------- 

    #     assign_today = assignment.objects.filter(date_from__gte=today_min)

    #     assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(date_from__lte=yesterday_max)
   
    #     proj_idds = []

    #     for update_s in assign_yestday:
    #         pro_ids = update_s.projectid
    #         proj_idds.append(pro_ids)

    #     pro_app= []

    #     for projs in proj_idds:
    #         pro_in = int(projs)
    #         pro_app.append(pro_in)

    #     empidappend = []

    #     for update_status in assign_today:
    #         empsids = update_status.employeeid
    #         empidappend.append(empsids)


    #     emptody_app= []

       
    #     for ints in empidappend:
    #         ints = int(ints)
    #         emptody_app.append(ints)
     
  

    #         # -------------------------------------------

    #     apppend_id = []
    #     active_emp_n = employee_details.objects.filter(status='Active').filter(role="IA")
    #     active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

    #     for i_d in active_emp_n:
          
    #         apppend_id.append(i_d.id)


    #     new_apend_data = [] 

    #     difference = set(emptody_app).symmetric_difference(set(apppend_id))
    #     list_difference = list(difference)

 
    #     active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)

    #     return render(request, "employee_register/assign_previous.html",{ 'emp_proj':id_filter,'date':yesterday})

    # else:
    #     if request.method == 'POST':
    #         recomme=request.POST.getlist('interest')
    #         platname = request.POST['options']

   
    #     new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    #     today1 = str(new_date)
    #     split_a = today1.split(".")
    #     split_date = split_a[0]
    #     split_date1 = str(split_date).split(" ")
    #     split_daten = split_date1[0]    

    #     today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    #     today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
       
    #     today = datetime.datetime.utcnow().date()

    #     yesterday = str(today - datetime.timedelta(days=1))

    #     srt_paqt = str(today_min)
    #     split_part = srt_paqt.split(' ')
    #     split_part[0] = yesterday
    #     yesterday_min = " ".join(map(str,split_part))

    #     if len(recomme) == 0:

    #         assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(projectid=platname)
    #         emy_id =[]
    #         for update_e in assign_yestday:
    #             empsids = update_e.employeeid
    #             emy_id.append(empsids)

    #         active_emp_yesterday = employee_details.objects.filter(pk__in=emy_id)

            

    #         active_emp_today = assignment.objects.filter(date_from__gte=today_min).filter(projectid=platname)
  
    #         emp_yest = []


    #         for stat_e in active_emp_yesterday:
    #             emp_ids = stat_e.id
    #             emp_yest.append(emp_ids)

    #         emptoday = []

    #         for stat_u in active_emp_today:
    #             emp_tody = stat_u.employeeid
    #             emptoday.append(emp_tody)
            
    #         emptoday_n = []    
    #         for ints in emptoday:
    #             ints = int(ints)
    #             emptoday_n.append(ints)
            
    #         difference = set(emp_yest).symmetric_difference(set(emptoday_n))
    #         list_difference = list(difference)
    #         emp_projs = projects.objects.filter(open_status__gte=today_min)
           
        
    #         new_updatestes = []
    #         for n_update in emp_projs:
    #             open_o = n_update.open_status 
    #             close_o = n_update.close_status
    #             if open_o and close_o == '':
    #                 open_d = n_update.id
    #                 new_updatestes.append(open_d)
                    
    #             else:
    #                 pass

    #         listsss =[platname]
        

                
    #         id_filter = projects.objects.filter(pk__in=listsss)
    #         active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
        

    #         active_emp = employee_details.objects.filter(pk__in=list_difference)
    #         platform_proj = projects.objects.filter(pk__in=listsss)
            

    #         return render(request, "employee_register/assign_previousdata.html",{'active_emp':active_emp,'active_tl':active_tl,'emp_proj':id_filter,'date':yesterday})
      
    #     else:
    #         if request.method == 'POST':

    #             recomme=request.POST.getlist('interest')
    #             platname = request.POST['options']
    #             tl_id = request.POST['option_tl']
    #         if platname == 'none' and tl_id =='none':
    #             return HttpResponse('DROPDOWN NOT SELECTED')
    #         else:    
    #             for index, item in enumerate(recomme):
    #                 new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    #                 today1 = str(new_date)
    #                 split_a = today1.split(".")
    #                 split_date = split_a[0]
    #                 split_date1 = str(split_date).split(" ")
    #                 split_daten = split_date1[0]
    #                 survey = assignment.objects.create(employeeid=item,projectid=platname,date_from=split_date,tl_id=tl_id)
           

    #             return render(request, "employee_register/assigned.html")            
            
            

def assigned(request):
    new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today1 = str(new_date)
    split_a = today1.split(".")
    split_date = split_a[0]
    split_date1 = str(split_date).split(" ")
    split_daten = split_date1[0]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
 
    assign_C = assignment.objects.filter(date_from__gte=today_min)

    tl1_ids = '528'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl1_ids)
    counts_ass = len(assign_C)

    main_ides = [] 
    empidappend =[]
    prjappend = []
    tl_ides = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend.append(empsids)
        
        projids = update_status.projectid
        prjappend.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides.append(tl_part)


    emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend)

    new_app =[]
    new_prj =[]
    tl_fulname =[]

    for piks in prjappend:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app.append(pname)
            plname = update.platform_name
            new_prj.append(plname)

 
    for tls in tl_ides:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment2 = assignment.objects.filter(from_to__gte=today_min)
    assignment2 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl1_ids)

    empidap =[]
    projap = []
    tls_part = []

    for upd_status in assignment2:
        
        emp_id = upd_status.employeeid
        empidap.append(emp_id)
        proj_id = upd_status.projectid
        projap.append(proj_id)
        tls = upd_status.tl_id
        tls_part.append(tls) 
    
    ressignm_det = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap)


    se_proj =[]
    se_plat =[]
    tl__fulname =[]

    for pi_ks in projap:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj.append(pname)
            plname = update_a.platform_name
            se_plat.append(plname)
            
    for tl_s in tls_part:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname.append(tl__name)


#=-============================================================================================================529 
    tl1_ids1 = '529'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl1_ids1)
    # counts_ass = len(assign)

    
    empidappend1 =[]
    prjappend1 = []
    tl_ides1 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend1.append(empsids)
        
        projids = update_status.projectid
        prjappend1.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides1.append(tl_part)


    emp_det_id1 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend1)

    new_app1 =[]
    new_prj1 =[]
    tl_fulname1 =[]

    for piks in prjappend1:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app1.append(pname)
            plname = update.platform_name
            new_prj1.append(plname)

 
    for tls in tl_ides1:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname1.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment2 = assignment.objects.filter(from_to__gte=today_min)
    assignment2 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl1_ids1)

    empidap1 =[]
    projap1 = []
    tls_part1 = []

    for upd_status in assignment2:
        
        emp_id = upd_status.employeeid
        empidap1.append(emp_id)
        proj_id = upd_status.projectid
        projap1.append(proj_id)
        tls = upd_status.tl_id
        tls_part1.append(tls)

    # print(empidap1)
    # print(projap1)
    # exit()     
    
    ressignm_det1 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap1)


    se_proj1 =[]
    se_plat1 =[]
    tl__fulname1 =[]
    for pi_ks in projap1:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj1.append(pname)
            plname = update_a.platform_name
            se_plat1.append(plname)
            
    for tl_s in tls_part1:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname1.append(tl__name)


#======================================================================================= 
    tl2_ids2 = '530'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl2_ids2)
    # counts_ass = len(assign)

    
    empidappend2 =[]
    prjappend2 = []
    tl_ides2 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend2.append(empsids)
        
        projids = update_status.projectid
        prjappend2.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides2.append(tl_part)


    emp_det_id2 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend2)

    new_app2 =[]
    new_prj2 =[]
    tl_fulname2 =[]

    for piks in prjappend2:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app2.append(pname)
            plname = update.platform_name
            new_prj2.append(plname)

 
    for tls in tl_ides2:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname2.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment2 = assignment.objects.filter(from_to__gte=today_min)
    assignment2 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl2_ids2)

    empidap2 =[]
    projap2 = []
    tls_part2 = []

    for upd_status in assignment2:
        
        emp_id = upd_status.employeeid
        empidap2.append(emp_id)
        proj_id = upd_status.projectid
        projap2.append(proj_id)
        tls = upd_status.tl_id
        tls_part2.append(tls)

    
    ressignm_det2 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap2)


    se_proj2 =[]
    se_plat2 =[]
    tl__fulname2 =[]
    for pi_ks in projap2:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj2.append(pname)
            plname = update_a.platform_name
            se_plat2.append(plname)
            
    for tl_s in tls_part2:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname2.append(tl__name)

#=============================================================================================
    tl3_ids3 = '531'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl3_ids3)
    # counts_ass = len(assign)

    
    empidappend3 =[]
    prjappend3 = []
    tl_ides3 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend3.append(empsids)
        
        projids = update_status.projectid
        prjappend3.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides3.append(tl_part)


    emp_det_id3 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend3)

    new_app3 =[]
    new_prj3 =[]
    tl_fulname3 =[]

    for piks in prjappend3:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app3.append(pname)
            plname = update.platform_name
            new_prj3.append(plname)

 
    for tls in tl_ides3:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname3.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment3 = assignment.objects.filter(from_to__gte=today_min)
    assignment3 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl3_ids3)

    empidap3 =[]
    projap3 = []
    tls_part3 = []

    for upd_status in assignment3:
        
        emp_id = upd_status.employeeid
        empidap3.append(emp_id)
        proj_id = upd_status.projectid
        projap3.append(proj_id)
        tls = upd_status.tl_id
        tls_part3.append(tls)

    
    ressignm_det3 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap3)


    se_proj3 =[]
    se_plat3 =[]
    tl__fulname3 =[]
    for pi_ks in projap3:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj3.append(pname)
            plname = update_a.platform_name
            se_plat3.append(plname)
            
    for tl_s in tls_part3:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname3.append(tl__name)

# ========================================================================================================

    tl4_ids4 = '532'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl4_ids4)
    # counts_ass = len(assign)

    
    empidappend4 =[]
    prjappend4 = []
    tl_ides4 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend4.append(empsids)
        
        projids = update_status.projectid
        prjappend4.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides4.append(tl_part)


    emp_det_id4 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend4)

    new_app4 =[]
    new_prj4 =[]
    tl_fulname4 =[]

    for piks in prjappend4:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app4.append(pname)
            plname = update.platform_name
            new_prj4.append(plname)

 
    for tls in tl_ides4:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname4.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment4 = assignment.objects.filter(from_to__gte=today_min)
    assignment4 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl4_ids4)

    empidap4 =[]
    projap4 = []
    tls_part4 = []

    for upd_status in assignment4:
        
        emp_id = upd_status.employeeid
        empidap4.append(emp_id)
        proj_id = upd_status.projectid
        projap4.append(proj_id)
        tls = upd_status.tl_id
        tls_part4.append(tls)

    
    ressignm_det4 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap4)


    se_proj4 =[]
    se_plat4 =[]
    tl__fulname4 =[]
    for pi_ks in projap4:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj4.append(pname)
            plname = update_a.platform_name
            se_plat4.append(plname)
            
    for tl_s in tls_part4:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname4.append(tl__name)


# ======================================================================

    tl5_ids5 = '533'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl5_ids5)
    # counts_ass = len(assign)

    
    empidappend5 =[]
    prjappend5 = []
    tl_ides5 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend5.append(empsids)
        
        projids = update_status.projectid
        prjappend5.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides5.append(tl_part)


    emp_det_id5 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend5)
    # print(emp_det_id5)
    # exit()

    new_app5 =[]
    new_prj5 =[]
    tl_fulname5 =[]

    for piks in prjappend5:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app5.append(pname)
            plname = update.platform_name
            new_prj5.append(plname)

 
    for tls in tl_ides5:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname5.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment5 = assignment.objects.filter(from_to__gte=today_min)
    assignment5 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl5_ids5)

    empidap5 =[]
    projap5 = []
    tls_part5 = []

    for upd_status in assignment5:
        
        emp_id = upd_status.employeeid
        empidap5.append(emp_id)
        proj_id = upd_status.projectid
        projap5.append(proj_id)
        tls = upd_status.tl_id
        tls_part5.append(tls)

    
    ressignm_det5 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap5)


    se_proj5 =[]
    se_plat5 =[]
    tl__fulname5 =[]
    for pi_ks in projap5:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj5.append(pname)
            plname = update_a.platform_name
            se_plat5.append(plname)
            
    for tl_s in tls_part5:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname5.append(tl__name)



#===================================================================================

    tl6_ids6 = '534'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl6_ids6)
    # counts_ass = len(assign)

    
    empidappend6 =[]
    prjappend6 = []
    tl_ides6 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend6.append(empsids)
        
        projids = update_status.projectid
        prjappend6.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides6.append(tl_part)


    emp_det_id6 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend6)
    # print(emp_det_id6)
    # exit()

    new_app6 =[]
    new_prj6 =[]
    tl_fulname6 =[]

    for piks in prjappend6:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app6.append(pname)
            plname = update.platform_name
            new_prj6.append(plname)

 
    for tls in tl_ides6:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname6.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment6 = assignment.objects.filter(from_to__gte=today_min)
    assignment6 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl6_ids6)

    empidap6 =[]
    projap6 = []
    tls_part6 = []

    for upd_status in assignment6:
        
        emp_id = upd_status.employeeid
        empidap6.append(emp_id)
        proj_id = upd_status.projectid
        projap6.append(proj_id)
        tls = upd_status.tl_id
        tls_part6.append(tls)

    
    ressignm_det6 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap6)


    se_proj6 =[]
    se_plat6 =[]
    tl__fulname6 =[]
    for pi_ks in projap6:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj6.append(pname)
            plname = update_a.platform_name
            se_plat6.append(plname)
            
    for tl_s in tls_part6:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname6.append(tl__name)


             #====================================================== 
    tl7_ids7 = '535'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl7_ids7)
    # counts_ass = len(assign)

    
    empidappend7 =[]
    prjappend7 = []
    tl_ides7 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend7.append(empsids)
        
        projids = update_status.projectid
        prjappend7.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides7.append(tl_part)


    emp_det_id7 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend7)
    # print(emp_det_id7)
    # exit()

    new_app7 =[]
    new_prj7 =[]
    tl_fulname7 =[]

    for piks in prjappend7:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app7.append(pname)
            plname = update.platform_name
            new_prj7.append(plname)

 
    for tls in tl_ides7:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname7.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment7 = assignment.objects.filter(from_to__gte=today_min)
    assignment7 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl7_ids7)

    empidap7 =[]
    projap7 = []
    tls_part7 = []

    for upd_status in assignment7:
        
        emp_id = upd_status.employeeid
        empidap7.append(emp_id)
        proj_id = upd_status.projectid
        projap7.append(proj_id)
        tls = upd_status.tl_id
        tls_part7.append(tls)

    
    ressignm_det7 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap7)


    se_proj7 =[]
    se_plat7 =[]
    tl__fulname7 =[]
    for pi_ks in projap7:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj7.append(pname)
            plname = update_a.platform_name
            se_plat7.append(plname)
            
    for tl_s in tls_part7:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname7.append(tl__name)         



# ===========================================================================
    tl8_ids8 = '536'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl7_ids7)
    # counts_ass = len(assign)

    
    empidappend8 =[]
    prjappend8 = []
    tl_ides8 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend8.append(empsids)
        
        projids = update_status.projectid
        prjappend8.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides8.append(tl_part)


    emp_det_id8 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend8)
    # print(emp_det_id8)
    # exit()

    new_app8 =[]
    new_prj8 =[]
    tl_fulname8 =[]

    for piks in prjappend8:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app8.append(pname)
            plname = update.platform_name
            new_prj8.append(plname)

 
    for tls in tl_ides8:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname8.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment8 = assignment.objects.filter(from_to__gte=today_min)
    assignment8 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl8_ids8)

    empidap8 =[]
    projap8 = []
    tls_part8 = []

    for upd_status in assignment8:
        
        emp_id = upd_status.employeeid
        empidap8.append(emp_id)
        proj_id = upd_status.projectid
        projap8.append(proj_id)
        tls = upd_status.tl_id
        tls_part8.append(tls)

    
    ressignm_det8 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap8)


    se_proj8 =[]
    se_plat8 =[]
    tl__fulname8 =[]
    for pi_ks in projap8:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj8.append(pname)
            plname = update_a.platform_name
            se_plat8.append(plname)
            
    for tl_s in tls_part8:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname8.append(tl__name)

#======================================================= 
    tl9_ids9 = '537'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl9_ids9)
    # counts_ass = len(assign)

    
    empidappend9 =[]
    prjappend9 = []
    tl_ides9 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend9.append(empsids)
        
        projids = update_status.projectid
        prjappend9.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides9.append(tl_part)


    emp_det_id9 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend9)
    # print(emp_det_id9)
    # exit()

    new_app9 =[]
    new_prj9 =[]
    tl_fulname9 =[]

    for piks in prjappend9:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app9.append(pname)
            plname = update.platform_name
            new_prj9.append(plname)

 
    for tls in tl_ides9:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname9.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment9 = assignment.objects.filter(from_to__gte=today_min)
    assignment9 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl9_ids9)

    empidap9 =[]
    projap9 = []
    tls_part9 = []

    for upd_status in assignment9:
        
        emp_id = upd_status.employeeid
        empidap9.append(emp_id)
        proj_id = upd_status.projectid
        projap9.append(proj_id)
        tls = upd_status.tl_id
        tls_part9.append(tls)

    
    ressignm_det9 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap9)


    se_proj9 =[]
    se_plat9 =[]
    tl__fulname9 =[]
    for pi_ks in projap9:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj9.append(pname)
            plname = update_a.platform_name
            se_plat9.append(plname)
            
    for tl_s in tls_part9:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname9.append(tl__name)

# =====================================================================================

    tl10_ids10 = '525'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl10_ids10)
    # counts_ass = len(assign)

    
    empidappend10 =[]
    prjappend10 = []
    tl_ides10 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend10.append(empsids)
        
        projids = update_status.projectid
        prjappend10.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides10.append(tl_part)


    emp_det_id10 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend10)
    # print(emp_det_id10)
    # exit()

    new_app10 =[]
    new_prj10 =[]
    tl_fulname10 =[]

    for piks in prjappend10:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app10.append(pname)
            plname = update.platform_name
            new_prj10.append(plname)

 
    for tls in tl_ides10:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname10.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment10 = assignment.objects.filter(from_to__gte=today_min)
    assignment10 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl10_ids10)

    empidap10 =[]
    projap10 = []
    tls_part10 = []

    for upd_status in assignment10:
        
        emp_id = upd_status.employeeid
        empidap10.append(emp_id)
        proj_id = upd_status.projectid
        projap10.append(proj_id)
        tls = upd_status.tl_id
        tls_part10.append(tls)

    
    ressignm_det10 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap10)


    se_proj10 =[]
    se_plat10 =[]
    tl__fulname10 =[]
    for pi_ks in projap10:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj10.append(pname)
            plname = update_a.platform_name
            se_plat10.append(plname)
            
    for tl_s in tls_part10:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname10.append(tl__name)

#=======================================================================================================
    tl11_ids11 = '526'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl11_ids11)
    # counts_ass = len(assign)

    
    empidappend11 =[]
    prjappend11 = []
    tl_ides11 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend11.append(empsids)
        
        projids = update_status.projectid
        prjappend11.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides11.append(tl_part)


    emp_det_id11 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend11)
    # print(emp_det_id11)
    # exit()

    new_app11 =[]
    new_prj11 =[]
    tl_fulname11 =[]

    for piks in prjappend11:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app11.append(pname)
            plname = update.platform_name
            new_prj11.append(plname)

 
    for tls in tl_ides11:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname11.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment11 = assignment.objects.filter(from_to__gte=today_min)
    assignment11 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl11_ids11)

    empidap11 =[]
    projap11 = []
    tls_part11 = []

    for upd_status in assignment11:
        
        emp_id = upd_status.employeeid
        empidap11.append(emp_id)
        proj_id = upd_status.projectid
        projap11.append(proj_id)
        tls = upd_status.tl_id
        tls_part11.append(tls)

    
    ressignm_det11 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap11)


    se_proj11 =[]
    se_plat11 =[]
    tl__fulname11 =[]
    for pi_ks in projap11:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj11.append(pname)
            plname = update_a.platform_name
            se_plat11.append(plname)
            
    for tl_s in tls_part11:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname11.append(tl__name)

#==================================================================================================
    
    tl12_ids12 = '527'
    
    # assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min)
    assign = assignment.objects.filter(first_work_done='').filter(date_from__gte=today_min).filter(tl_id=tl12_ids12)
    # counts_ass = len(assign)

    
    empidappend12 =[]
    prjappend12 = []
    tl_ides12 = []

    for update_status in assign:
        empsids = update_status.employeeid
        empidappend12.append(empsids)
        
        projids = update_status.projectid
        prjappend12.append(projids)
        
        tl_part = update_status.tl_id
        tl_ides12.append(tl_part)


    emp_det_id12 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend12)
    # print(emp_det_id12)
    # exit()

    new_app12 =[]
    new_prj12 =[]
    tl_fulname12 =[]

    for piks in prjappend12:
        proj_det_id = projects.objects.filter(id=piks)
        for update in proj_det_id:
            pname = update.project_name
            new_app12.append(pname)
            plname = update.platform_name
            new_prj12.append(plname)

 
    for tls in tl_ides12:
        tl_idfs = employee_details.objects.filter(id=tls)
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname12.append(tl_name)
 

    # ------------------------------------Ressign part-----------------------------------
    # assignment12 = assignment.objects.filter(from_to__gte=today_min)
    assignment12 = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl12_ids12)

    empidap12 =[]
    projap12 = []
    tls_part12 = []

    for upd_status in assignment12:
        
        emp_id = upd_status.employeeid
        empidap12.append(emp_id)
        proj_id = upd_status.projectid
        projap12.append(proj_id)
        tls = upd_status.tl_id
        tls_part12.append(tls)

    
    ressignm_det12 = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap12)


    se_proj12 =[]
    se_plat12 =[]
    tl__fulname12 =[]
    for pi_ks in projap12:
       
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj12.append(pname)
            plname = update_a.platform_name
            se_plat12.append(plname)
            
    for tl_s in tls_part12:
        tl__idfs = employee_details.objects.filter(id=tl_s)
    
        for up__tl in tl__idfs:
            tl__name = up__tl.full_name
            tl__fulname12.append(tl__name) 
    

 
  # 'emp_det_id1':emp_det_id1,'new_app1':new_app1,'new_prj1':new_prj1,'tl_fulname1':tl_fulname1,
  # 'ressignm_det1':ressignm_det1,'se_proj1':se_proj1,'se_plat1':se_plat1,'tl__fulname1':tl__fulname1,


  # 'emp_det_id12':emp_det_id12,'new_app12':new_app12,'new_prj12':new_prj12,'tl_fulname12':tl_fulname12,'ressignm_det12':ressignm_det12,'se_proj12':se_proj12,'se_plat12':se_plat12,'tl__fulname12':tl__fulname12,



    


    return render(request, "employee_register/assigned.html",{'emp_det_id12':emp_det_id12,'new_app12':new_app12,'new_prj12':new_prj12,'tl_fulname12':tl_fulname12,'ressignm_det12':ressignm_det12,'se_proj12':se_proj12,'se_plat12':se_plat12,'tl__fulname12':tl__fulname12,'emp_det_id11':emp_det_id11,'new_app11':new_app11,'new_prj11':new_prj11,'tl_fulname11':tl_fulname11,'ressignm_det11':ressignm_det11,'se_proj11':se_proj11,'se_plat11':se_plat11,'tl__fulname11':tl__fulname11,'emp_det_id10':emp_det_id10,'new_app10':new_app10,'new_prj10':new_prj10,'tl_fulname10':tl_fulname10,'ressignm_det10':ressignm_det10,'se_proj10':se_proj10,'se_plat10':se_plat10,'tl__fulname10':tl__fulname10,'emp_det_id9':emp_det_id9,'new_app9':new_app9,'new_prj9':new_prj9,'tl_fulname9':tl_fulname9,'ressignm_det9':ressignm_det9,'se_proj9':se_proj9,'se_plat9':se_plat9,'tl__fulname9':tl__fulname9,'emp_det_id8':emp_det_id8,'new_app8':new_app8,'new_prj8':new_prj8,'tl_fulname8':tl_fulname8,'ressignm_det8':ressignm_det8,'se_proj8':se_proj8,'se_plat8':se_plat8,'tl__fulname8':tl__fulname8,'emp_det_id7':emp_det_id7,'new_app7':new_app7,'new_prj7':new_prj7,'tl_fulname7':tl_fulname7,'ressignm_det7':ressignm_det7,'se_proj7':se_proj7,'se_plat7':se_plat7,'tl__fulname7':tl__fulname7,'emp_det_id6':emp_det_id6,'new_app6':new_app6,'new_prj6':new_prj6,'tl_fulname6':tl_fulname6,'ressignm_det6':ressignm_det6,'se_proj6':se_proj6,'se_plat6':se_plat6,'tl__fulname6':tl__fulname6,'emp_det_id5':emp_det_id5,'new_app5':new_app5,'new_prj5':new_prj5,'tl_fulname5':tl_fulname5,'ressignm_det5':ressignm_det5,'se_proj5':se_proj5,'se_plat5':se_plat5,'tl__fulname5':tl__fulname5,'emp_det_id4':emp_det_id4,'new_app4':new_app4,'new_prj4':new_prj4,'tl_fulname4':tl_fulname4,'ressignm_det4':ressignm_det4,'se_proj4':se_proj4,'se_plat4':se_plat4,'tl__fulname4':tl__fulname4,'emp_det_id3':emp_det_id3,'new_app3':new_app3,'new_prj3':new_prj3,'tl_fulname3':tl_fulname3,'ressignm_det3':ressignm_det3,'se_proj3':se_proj3,'se_plat3':se_plat3,'tl__fulname3':tl__fulname3,'emp_det_id2':emp_det_id2,'new_app2':new_app2,'new_prj2':new_prj2,'tl_fulname2':tl_fulname2,'ressignm_det2':ressignm_det2,'se_proj2':se_proj2,'se_plat2':se_plat2,'tl__fulname2':tl__fulname2,'emp_det_id1':emp_det_id1,'new_app1':new_app1,'new_prj1':new_prj1,'tl_fulname1':tl_fulname1,'ressignm_det1':ressignm_det1,'se_proj1':se_proj1,'se_plat1':se_plat1,'tl__fulname1':tl__fulname1,'emp_det':emp_det_id,'proj_name':new_app,'pla_name':new_prj,'ressignm_det':ressignm_det,'se_proj':se_proj,'se_plat':se_plat,'date':split_daten, 'tl_fulname':tl_fulname,'tl__fulname':tl__fulname, 'counts_ass':counts_ass})            



       
# def assigned(request):
#     new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
#     today1 = str(new_date)
#     split_a = today1.split(".")
#     split_date = split_a[0]
#     split_date1 = str(split_date).split(" ")
#     split_daten = split_date1[0]
#     today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
 
#     assign = assignment.objects.filter(date_from__gte=today_min)
#     counts_ass = len(assign)

#     active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
#     tl_emp =[]
    
    

    
#     app__proj1 = []
#     app__pla1 = []
#     fnames1 =[]

#     app__proj2 = []
#     app__pla2 = []
#     fnames2 =[]

#     app__proj3 = []
#     app__pla3 = []
#     fnames3 =[]

#     app__proj4 = []
#     app__pla4 = []
#     fnames4 =[]


#     app__proj5 = []
#     app__pla5 = []
#     fnames5 =[]

#     app__proj6 = []
#     app__pla6 = []
#     fnames6 =[]

#     app__proj7 = []
#     app__pla7 = []
#     fnames7 =[]

#     app__proj8 = []
#     app__pla8 = []
#     fnames8 =[]

#     app__proj9 = []
#     app__pla9 = []
#     fnames9 =[]

#     app__proj10 = []
#     app__pla10 = []
#     fnames10 =[]

#     app__proj11 = []
#     app__pla11 = []
#     fnames11 =[]

#     app__proj12 = []
#     app__pla12 = []
#     fnames12 =[]

#     app__proj13 = []
#     app__pla13 = []
#     fnames13 =[]

#     for tlms in active_tl:
#         tl_l = tlms.id
#         tl_emp.append(tl_l)
 
#     for v_s in assign:
#         tl_i1 = v_s.tl_id
        
#         if tl_i1 == '528':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj1.append(pr_name)
#                 app__pla1.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames1.append(fnamsses1)


#         if tl_i1 == '529':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names1 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj2.append(pr_name)
#                 app__pla2.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames2.append(fnamsses1)


#         if tl_i1 == '530':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names2 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj3.append(pr_name)
#                 app__pla3.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames3.append(fnamsses1)


#         if tl_i1 == '531':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names3 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj4.append(pr_name)
#                 app__pla4.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames4.append(fnamsses1)


#         if tl_i1 == '532':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names4 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj5.append(pr_name)
#                 app__pla5.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames5.append(fnamsses1)
        

#         if tl_i1 == '533':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names5 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj6.append(pr_name)
#                 app__pla6.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames6.append(fnamsses1)


#         if tl_i1 == '534':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names6 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj7.append(pr_name)
#                 app__pla7.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames7.append(fnamsses1)
                
#         if tl_i1 == '535':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names7 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj8.append(pr_name)
#                 app__pla8.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames8.append(fnamsses1) 
                
#         if tl_i1 == '536':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names8 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj9.append(pr_name)
#                 app__pla9.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames9.append(fnamsses1)
                
#         if tl_i1 == '537':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names9 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj10.append(pr_name)
#                 app__pla10.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames10.append(fnamsses1)


#         if tl_i1 == '525':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names10 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj11.append(pr_name)
#                 app__pla11.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames11.append(fnamsses1)
                

#         if tl_i1 == '526':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names11 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj12.append(pr_name)
#                 app__pla12.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames12.append(fnamsses1)
 


#         if tl_i1 == '527':
#             project___id = v_s.projectid
#             empss__id = v_s.employeeid
#             emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            
#             for nams in emp_tl_id:
#                 names12 = nams['full_name']
            
#             proj__id = projects.objects.filter(id=project___id)
#             for pr in proj__id:
#                 pr_name = pr.project_name 
#                 pl_name = pr.platform_name
#                 app__proj13.append(pr_name)
#                 app__pla13.append(pl_name)
            
            
#             employ_id = employee_details.objects.filter(id=empss__id)
#             for namesd1 in employ_id:
#                 fnamsses1 = namesd1.full_name +"---"+namesd1.mobile
#                 fnames13.append(fnamsses1) 





    

#     if len(fnames1) == 0:
#         proj1 = ""
#         plat1 = ""
#         empnames1 = ""
#         new_tl1 = ""
        
#     else:
#         tl_names1 = names
#         proj1 = app__proj1
#         plat1 = app__pla1
#         empnames1 =fnames1
#         check_length = len(empnames1)
#         given_value =tl_names1
#         new_tl1=[]
#         new_tl1.extend(repeat(given_value,check_length))


#     if len(fnames2) == 0:
#         proj2 = ""
#         plat2 = ""
#         empnames2 = ""
#         new_tl2 = ""
        
#     else:
#         tl_names2 = names1
#         proj2 = app__proj2
#         plat2 = app__pla2
#         empnames2 = fnames2
#         check_length2 = len(empnames2)
#         given_value2 =tl_names2
#         new_tl2=[]
#         new_tl2.extend(repeat(given_value2,check_length2))


#     if len(fnames3) == 0:
#         proj3 = ""
#         plat3 = ""
#         empnames3 = ""
#         new_tl3 = ""
        
#     else:
#         tl_names3 = names2
#         proj3 = app__proj3
#         plat3 = app__pla3
#         empnames3 = fnames3
#         check_length3 = len(empnames3)
#         given_value3 =tl_names3
#         new_tl3=[]
#         new_tl3.extend(repeat(given_value3,check_length3))


#     if len(fnames4) == 0:
#         proj4 = ""
#         plat4 = ""
#         empnames4 = ""
#         new_tl4 = ""
        
#     else:
#         tl_names4 = names3
#         proj4 = app__proj4
#         plat4 = app__pla4
#         empnames4 = fnames4
#         check_length4 = len(empnames4)
#         given_value4 =tl_names4
#         new_tl4=[]
#         new_tl4.extend(repeat(given_value4,check_length4))


#     if len(fnames5) == 0:
#         proj5 = ""
#         plat5 = ""
#         empnames5 = ""
#         given_value5 =tl_names5
#         new_tl5=[]
#         new_tl5.extend(repeat(given_value5,check_length5))



#     if len(fnames6) == 0:
#         proj6 = ""
#         plat6 = ""
#         empnames6 = ""
#         new_tl6 = ""
        
#     else:
#         tl_names6 = names5
#         proj6 = app__proj6
#         plat6 = app__pla6
#         empnames6 = fnames6
#         check_length6 = len(empnames6)
#         given_value6 =tl_names6
#         new_tl6=[]
#         new_tl6.extend(repeat(given_value6,check_length6))                    

#     if len(fnames7) == 0:
#         proj7 = ""
#         plat7 = ""
#         empnames7 = ""
#         new_tl7 = ""
        
#     else:
#         tl_names7 = names6
#         proj7 = app__proj7
#         plat7 = app__pla7
#         empnames7 = fnames7
#         check_length7 = len(empnames7)
#         given_value7 =tl_names7
#         new_tl7=[]
#         new_tl7.extend(repeat(given_value7,check_length7))

#     if len(fnames8) == 0:
#         proj8 = ""
#         plat8 = ""
#         empnames8 = ""
#         new_tl8 = ""
        
#     else:
#         tl_names8 = names7
#         proj8 = app__proj8
#         plat8 = app__pla8
#         empnames8 = fnames8
#         check_length8 = len(empnames8)
#         given_value8 =tl_names8
#         new_tl8=[]
#         new_tl8.extend(repeat(given_value8,check_length8))


#     if len(fnames9) == 0:
#         proj9 = ""
#         plat9 = ""
#         empnames9 = ""
#         new_tl9 = ""
        
#     else:
#         tl_names9 = names8
#         proj9 = app__proj5
#         plat9 = app__pla9
#         empnames9 = fnames9
#         check_length9 = len(empnames9)
#         given_value9 =tl_names9
#         new_tl9=[]
#         new_tl9.extend(repeat(given_value9,check_length9))
        
#     if len(fnames10) == 0:
#         proj10 = ""
#         plat10 = ""
#         empnames10 = ""
#         new_tl10 = ""
        
#     else:
#         tl_names10 = names9
#         proj10 = app__proj10
#         plat10 = app__pla10
#         empnames10 = fnames10
#         check_length10 = len(empnames10)
#         given_value10 =tl_names10
#         new_tl10=[]
#         new_tl10.extend(repeat(given_value10,check_length10))
        

#     if len(fnames11) == 0:
#         proj11 = ""
#         plat11 = ""
#         empnames11 = ""
#         new_tl11 = ""
        
#     else:
#         tl_names11 = names10
#         proj11 = app__proj11
#         plat11 = app__pla11
#         empnames11 = fnames11
#         check_length11 = len(empnames11)
#         given_value11 =tl_names11
#         new_tl11=[]
#         new_tl11.extend(repeat(given_value11,check_length11))
        


#     if len(fnames12) == 0:
#         proj12 = ""
#         plat12 = ""
#         empnames12 = ""
#         new_tl12 = ""
        
#     else:
#         tl_names12 = names11
#         proj12 = app__proj12
#         plat12 = app__pla12
#         empnames12 = fnames12
#         check_length12 = len(empnames12)
#         given_value12 =tl_names12
#         new_tl12=[]
#         new_tl12.extend(repeat(given_value12,check_length12))
        

#     if len(fnames13) == 0:
#         proj13 = ""
#         plat13 = ""
#         empnames13 = ""
#         new_tl13 = ""
        
#     else:
#         tl_names13 = names12
#         proj13 = app__proj13
#         plat13 = app__pla13
#         empnames13 = fnames13
#         check_length13 = len(empnames13)
#         given_value13 =tl_names13
#         new_tl13=[]
#         new_tl13.extend(repeat(given_value13,check_length13)) 


#     #================== skip parts ===================================
#     employee_id = []
#     emps__nsids1 = []
#     app__projs1 =[]    
 

#     empidappend =[]
#     prjappend = []
#     tl_ides = []




#     for update_status in assign:
        
#         empsids = update_status.employeeid
#         empidappend.append(empsids)
#         projids = update_status.projectid
#         prjappend.append(projids)
        
#         tl_part = update_status.tl_id
#         tl_ides.append(tl_part)
    

#     int__d = []

#     for emp_dts in empidappend:
#         emp_in = int(emp_dts)
#         int__d.append(emp_in)

#     new_app =[]
#     new_prj =[]
#     tl_fulname =[]

#     for piks in prjappend:
#         proj_det_id = projects.objects.filter(id=piks)
#         for update in proj_det_id:
#             pname = update.project_name
#             new_app.append(pname)
#             plname = update.platform_name
#             new_prj.append(plname)

#     for tls in tl_ides:
#         tl_idfs = employee_details.objects.filter(id=tls)
#         for up_tl in tl_idfs:
#             tl_name = up_tl.full_name
#             tl_fulname.append(tl_name)    


#     assignment2 = assignment.objects.filter(from_to__gte=today_min)

#     empidap =[]
#     projap = []
#     tls_part = []

#     for upd_status in assignment2:
        
#         emp_id = upd_status.employeeid
#         empidap.append(emp_id)
#         proj_id = upd_status.projectid
#         projap.append(proj_id)
#         tls = upd_status.tl_id
#         tls_part.append(tls) 

#     int_rec__d = []

#     for emp_rec_dts in empidap:
#         emp_rec_in = int(emp_rec_dts)
#         int_rec__d.append(emp_rec_in)



#     difference = set(int__d).symmetric_difference(set(int_rec__d))
#     list_difference = list(difference) 

#     elements_in_all = list(set.intersection(*map(set, [int__d, int_rec__d])))


#     len_main = len(list_difference)
#     projs  = len(new_app)
#     pla = len(new_prj)



#     count_diff = projs - len_main


#     if len(assignment2) == 0:
#         new_app = new_app
#         new_prj = new_prj
#         tl_fulname = tl_fulname
#     else:
#         del new_app[-count_diff:]
#         del new_prj[-count_diff:]
#         del tl_fulname[-count_diff:]

#     emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=list_difference)
#     ressignm_det = employee_details.objects.values('full_name','mobile').filter(pk__in=elements_in_all)

#     se_proj =[]
#     se_plat =[]
#     tl__fulname =[]

#     for pi_ks in projap:
        
#         proj_de_id = projects.objects.filter(id=pi_ks)
        
#         for update_a in proj_de_id:
#             pname = update_a.project_name
#             se_proj.append(pname)
#             plname = update_a.platform_name
#             se_plat.append(plname)
            
#     for tl_s in tls_part:
#         tl__idfs = employee_details.objects.filter(id=tl_s)
    
#         for up__tl in tl__idfs:
#             tl__name = up__tl.full_name
#             tl__fulname.append(tl__name)
#         new_tl5 = ""
        
#     else:
#         tl_names5 = names4
#         proj5 = app__proj5
#         plat5 = app__pla5
#         empnames5 = fnames5
#         check_length5 = len(empnames5)

#     # skip parts ===================================              






#     # return render(request, "employee_register/assigned.html",{'new_tl13':new_tl13, 'proj13':proj13, 'plat13':plat13, 'empnames13':empnames13,'new_tl12':new_tl12, 'proj12':proj12, 'plat12':plat12, 'empnames12':empnames12,'new_tl11':new_tl11, 'proj11':proj11, 'plat11':plat11, 'empnames11':empnames11,'new_tl10':new_tl10, 'proj10':proj10, 'plat10':plat10, 'empnames10':empnames10,'new_tl9':new_tl9, 'proj9':proj9, 'plat9':plat9, 'empnames9':empnames9,'new_tl8':new_tl8, 'proj8':proj8, 'plat8':plat8, 'empnames8':empnames8,'new_tl7':new_tl7, 'proj7':proj7, 'plat7':plat7, 'empnames7':empnames7,'new_tl6':new_tl6, 'proj6':proj6, 'plat6':plat6, 'empnames6':empnames6,'new_tl5':new_tl5, 'proj5':proj5, 'plat5':plat5, 'empnames5':empnames5,'new_tl4':new_tl4, 'proj4':proj4, 'plat4':plat4, 'empnames4':empnames4,'new_tl1':new_tl1, 'proj1':proj1, 'plat1':plat1, 'empnames1':empnames1,'new_tl2':new_tl2, 'proj2':proj2, 'plat2':plat2, 'empnames2':empnames2,'new_tl3':new_tl3, 'proj3':proj3, 'plat3':plat3, 'empnames3':empnames3})
    




    


  

    



    

   





#    # 'new_tl3':new_tl3, 'proj3':proj3, 'plat3':plat3, 'empnames3':empnames3,
#    # 'new_tl4':new_tl4, 'proj4':proj4, 'plat4':plat4, 'empnames4':empnames4,
#    # 'new_tl5':new_tl5, 'proj5':proj5, 'plat5':plat5, 'empnames5':empnames5,
#    # 'new_tl6':new_tl6, 'proj6':proj6, 'plat6':plat6, 'empnames6':empnames6,
#    # 'new_tl7':new_tl7, 'proj7':proj7, 'plat7':plat7, 'empnames7':empnames7,
#    # 'new_tl8':new_tl8, 'proj8':proj8, 'plat8':plat8, 'empnames8':empnames8,
#    # 'new_tl9':new_tl9, 'proj9':proj9, 'plat9':plat9, 'empnames9':empnames9,
#    # 'new_tl10':new_tl10, 'proj10':proj10, 'plat10':plat10, 'empnames10':empnames10,
#    # 'new_tl11':new_tl11, 'proj11':proj11, 'plat11':plat11, 'empnames11':empnames11,
#    # 'new_tl12':new_tl12, 'proj12':proj12, 'plat12':plat12, 'empnames12':empnames12,
#    # 'new_tl13':new_tl13, 'proj13':proj13, 'plat13':plat13, 'empnames13':empnames13,



#     # print(tl_names)
#     # print(proj)
#     # print(plat)
#     # print(empnames)




                
               
             

           


                
    
               
    
    










#     # employee_id = []
#     # emps__nsids1 = []
#     # app__projs1 =[]    
 

#     # empidappend =[]
#     # prjappend = []
#     # tl_ides = []




#     # for update_status in assign:
        
#     #     empsids = update_status.employeeid
#     #     empidappend.append(empsids)
#     #     projids = update_status.projectid
#     #     prjappend.append(projids)
        
#     #     tl_part = update_status.tl_id
#     #     tl_ides.append(tl_part)
    

#     # int__d = []

#     # for emp_dts in empidappend:
#     #     emp_in = int(emp_dts)
#     #     int__d.append(emp_in)

#     # new_app =[]
#     # new_prj =[]
#     # tl_fulname =[]

#     # for piks in prjappend:
#     #     proj_det_id = projects.objects.filter(id=piks)
#     #     for update in proj_det_id:
#     #         pname = update.project_name
#     #         new_app.append(pname)
#     #         plname = update.platform_name
#     #         new_prj.append(plname)

#     # for tls in tl_ides:
#     #     tl_idfs = employee_details.objects.filter(id=tls)
#     #     for up_tl in tl_idfs:
#     #         tl_name = up_tl.full_name
#     #         tl_fulname.append(tl_name)


            




#     # # ------------------------------------Ressign part-----------------------------------
#     # assignment2 = assignment.objects.filter(from_to__gte=today_min)

#     # empidap =[]
#     # projap = []
#     # tls_part = []

#     # for upd_status in assignment2:
        
#     #     emp_id = upd_status.employeeid
#     #     empidap.append(emp_id)
#     #     proj_id = upd_status.projectid
#     #     projap.append(proj_id)
#     #     tls = upd_status.tl_id
#     #     tls_part.append(tls) 

#     # int_rec__d = []

#     # for emp_rec_dts in empidap:
#     #     emp_rec_in = int(emp_rec_dts)
#     #     int_rec__d.append(emp_rec_in)



#     # difference = set(int__d).symmetric_difference(set(int_rec__d))
#     # list_difference = list(difference) 

#     # elements_in_all = list(set.intersection(*map(set, [int__d, int_rec__d])))


#     # len_main = len(list_difference)
#     # projs  = len(new_app)
#     # pla = len(new_prj)



#     # count_diff = projs - len_main


#     # if len(assignment2) == 0:
#     #     new_app = new_app
#     #     new_prj = new_prj
#     #     tl_fulname = tl_fulname
#     # else:
#     #     del new_app[-count_diff:]
#     #     del new_prj[-count_diff:]
#     #     del tl_fulname[-count_diff:]

#     # emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=list_difference)
#     # ressignm_det = employee_details.objects.values('full_name','mobile').filter(pk__in=elements_in_all)

#     # se_proj =[]
#     # se_plat =[]
#     # tl__fulname =[]

#     # for pi_ks in projap:
        
#     #     proj_de_id = projects.objects.filter(id=pi_ks)
        
#     #     for update_a in proj_de_id:
#     #         pname = update_a.project_name
#     #         se_proj.append(pname)
#     #         plname = update_a.platform_name
#     #         se_plat.append(plname)
            
#     # for tl_s in tls_part:
#     #     tl__idfs = employee_details.objects.filter(id=tl_s)
    
#     #     for up__tl in tl__idfs:
#     #         tl__name = up__tl.full_name
#     #         tl__fulname.append(tl__name)



#     # return render(request, "employee_register/assigned.html",{'emp_det':emp_det_id,'proj_name':new_app,'pla_name':new_prj,'ressignm_det':ressignm_det,'se_proj':se_proj,'se_plat':se_plat,'date':split_daten, 'tl_fulname':tl_fulname,'tl__fulname':tl__fulname, 'counts_ass':counts_ass})



def project_close(request):

    if request.method == "GET":

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]

        
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]

        # context ={}
        # context["dataset"] = projects.objects.filter(open_status__gte=today_min)

        
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        emp_projs = projects.objects.all()
        new_updatestes = []


        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status

            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                

            else:
                open_d = n_update.id
                print(open_d)
                

        id_filter = projects.objects.filter(pk__in=new_updatestes)


        return render(request, "employee_register/project_close.html",{'dataset':id_filter})
        
    else:
      

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        projnm=request.POST.getlist('interest')
        # projnm = request.POST['pros']

        # print(projnm)
        # exit()

        types_chng = []    
        for ints in projnm:
            ints = int(ints)
            types_chng.append(ints)

        
        
        emp_det = projects.objects.all()
        new_apps = []

        
        
        for piks in types_chng:
      
            proj_det_id = projects.objects.filter(id=piks)
  
            
            for update_time in proj_det_id:
                pname = update_time.id
                if pname:
                    update_time.close_status = split_date
                    update_time.save()
                else:
                    pass
   
        return render(request, "employee_register/project_close.html")    




def create_person(request):
     if request.method == "GET":
        form = EmployeeInserForm()
        return render(request, "employee_register/create_person.html",{'form': form})
     else:
        form = EmployeeInserForm(request.POST)
        if form.is_valid():
            form.save()
        
        return render(request, "employee_register/create_person.html")


def overall_data(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today1 = str(today_date)
    split_a = today1.split(".")
    split_date = split_a[0]
    split_date1 = str(split_date).split(" ")
    split_daten =split_date1[0]
    

    assigns__n = assignment.objects.filter(date_from__gte=today_min).filter(first_work_done='')

    assigns__second = assignment.objects.filter(from_to__gte=today_min)

    # print(assigns__second)
    # exit()
    counts_people = len(assigns__n)
    
    emps__nsids1 = []
    app__projs1 = []
    
    emps__nsid2 = []
    app__projs2 = []

    emps__nsid3 = []
    app__projs3 = []

    emps__nsid4 = []
    app__projs4 = []

    emps__nsid5 = []
    app__projs5 = []

    emps__nsid6 = []
    app__projs6 = []

    emps__nsid7 = []
    app__projs7 = []

    emps__nsid8 = []
    app__projs8 = []

    emps__nsid9 = []
    app__projs9 = []

    emps__nsid10 = []
    app__projs10 = []

    emps__nsid11 = []
    app__projs11 = []

    emps__nsid12 = []
    app__projs12 = []

    emps__nsid13 = []
    app__projs13 = []



    # +++++++++++++++second++++++++++++++++++++++++++++++++
    emps__sec1 = []
    app__prosce1 = []
    
    emps__sec2 = []
    app__prosce2 = []

    emps__sec3 = []
    app__prosce3 = []

    emps__sec4 = []
    app__prosce4 = []

    emps__sec5 = []
    app__prosce5 = []

    emps__sec6 = []
    app__prosce6 = []

    emps__sec7 = []
    app__prosce7 = []

    emps__sec8 = []
    app__prosce8 = []

    emps__sec9 = []
    app__prosce9 = []
    
    emps__sec10 = []
    app__prosce10 = []

    emps__sec11 = []
    app__prosce11 = []

    emps__sec12 = []
    app__prosce12 = []

    emps__sec13 = []
    app__prosce13 = []


    #+++++++++++++++++++++++++++++++++++++++++++++++


    active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
    tl_emp =[]
    
    

    for tlms in active_tl:
        tl_l = tlms.id
        tl_emp.append(tl_l)
 
    for v_s in assigns__n:
        tl_i1 = v_s.tl_id
        
        if tl_i1 == '528':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsids1.append(empss__id)
            emp_tl_id = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_id:
                names = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + '----' + pr.platform_name
                app__projs1.append(pr_name)

        if tl_i1 == '532':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid2.append(empss__id)
            emp_tl_2s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_2s:
                names_2s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs2.append(pr_name)
            
        if tl_i1 == '529':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid3.append(empss__id)
            emp_tl_3s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_3s:
                names_3s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs3.append(pr_name)

        if tl_i1 == '530':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid4.append(empss__id)
            emp_tl_4s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_4s:
                names_4s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs4.append(pr_name)



        if tl_i1 == '531':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid5.append(empss__id)
            emp_tl_5s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_5s:
                names_5s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs5.append(pr_name)



        if tl_i1 == '533':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid6.append(empss__id)
            emp_tl_6s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_6s:
                names_6s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs6.append(pr_name)

        if tl_i1 == '534':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid7.append(empss__id)
            emp_tl_7s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_7s:
                names_7s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs7.append(pr_name)

        if tl_i1 == '535':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid8.append(empss__id)
            emp_tl_8s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_8s:
                names_8s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs8.append(pr_name)
                

        if tl_i1 == '536':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid9.append(empss__id)
            emp_tl_9s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_9s:
                names_9s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs9.append(pr_name)
                

        if tl_i1 == '537':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid10.append(empss__id)
            emp_tl_10s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_10s:
                names_10s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs10.append(pr_name)  

        if tl_i1 == '525':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid11.append(empss__id)
            emp_tl_11s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_11s:
                names_11s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs11.append(pr_name)

        if tl_i1 == '526':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid12.append(empss__id)
            emp_tl_12s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_12s:
                names_12s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs12.append(pr_name)

        if tl_i1 == '527':
            project___id = v_s.projectid
            empss__id = v_s.employeeid
            emps__nsid13.append(empss__id)
            emp_tl_13s = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams in emp_tl_13s:
                names_13s = nams['full_name']
            proj__id = projects.objects.filter(id=project___id)
            for pr in proj__id:
                pr_name = pr.project_name + "---" +pr.platform_name
                app__projs13.append(pr_name)

# ============second====================================

    for v_d in assigns__second:
        tl_i1 = v_d.tl_id
        if tl_i1 == '528':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec1.append(emp_sec__id)
            emp_tl_sec1 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec1 in emp_tl_sec1:
                names_sec1 = nams_sec1['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce1.append(pr_sec_name)


        if tl_i1 == '532':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec2.append(emp_sec__id)
            emp_tl_sec2 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec2 in emp_tl_sec2:
                names_sec2 = nams_sec2['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce2.append(pr_sec_name)
                
        if tl_i1 == '529':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec3.append(emp_sec__id)
            emp_tl_sec3 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec3 in emp_tl_sec3:
                names_sec3 = nams_sec3['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce3.append(pr_sec_name)
                


        if tl_i1 == '530':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec4.append(emp_sec__id)
            emp_tl_sec4 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec4 in emp_tl_sec4:
                names_sec4 = nams_sec4['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce4.append(pr_sec_name)
                
        if tl_i1 == '531':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec5.append(emp_sec__id)
            emp_tl_sec5 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec5 in emp_tl_sec5:
                names_sec5 = nams_sec5['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce5.append(pr_sec_name)
                

        if tl_i1 == '533':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec6.append(emp_sec__id)
            emp_tl_sec6 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec6 in emp_tl_sec6:
                names_sec6 = nams_sec6['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce6.append(pr_sec_name)
                
        if tl_i1 == '534':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec7.append(emp_sec__id)
            emp_tl_sec7 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec7 in emp_tl_sec7:
                names_sec7 = nams_sec7['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce7.append(pr_sec_name)

        if tl_i1 == '535':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec8.append(emp_sec__id)
            emp_tl_sec8 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec8 in emp_tl_sec8:
                names_sec8 = nams_sec8['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce8.append(pr_sec_name)
                
        if tl_i1 == '536':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec9.append(emp_sec__id)
            emp_tl_sec9 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec9 in emp_tl_sec9:
                names_sec9 = nams_sec9['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce9.append(pr_sec_name)
        
        if tl_i1 == '537':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec10.append(emp_sec__id)
            emp_tl_sec10 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec10 in emp_tl_sec10:
                names_sec10 = nams_sec10['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce10.append(pr_sec_name)

        if tl_i1 == '525':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec11.append(emp_sec__id)
            emp_tl_sec11 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec11 in emp_tl_sec11:
                names_sec11 = nams_sec11['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce11.append(pr_sec_name)


        if tl_i1 == '526':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec12.append(emp_sec__id)
            emp_tl_sec12 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec12 in emp_tl_sec12:
                names_sec12 = nams_sec12['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce12.append(pr_sec_name)
        

        if tl_i1 == '527':
            project_sec___id = v_d.projectid
            emp_sec__id = v_d.employeeid
            emps__sec13.append(emp_sec__id)
            emp_tl_sec13 = employee_details.objects.values('full_name').filter(id=tl_i1)
            for nams_sec13 in emp_tl_sec13:
                names_sec13 = nams_sec13['full_name']
            proj_sec__id = projects.objects.filter(id=project_sec___id)
            for pr in proj_sec__id:
                pr_sec_name = pr.project_name + '----' + pr.platform_name
                app__prosce13.append(pr_sec_name)
        
        


      


            
#===========================second====================
    counts___1 = Counter(app__prosce1)
    ress1 = []
    for i in app__prosce1:
        if i not in ress1:
            ress1.append(i)
    resst1 = ress1
    projs___1 = []
    plats___1 = []

    for color1 in resst1:
         project = color1
         projs___1.append(project)
         Platform = counts___1[color1]
         plats___1.append(Platform)

    if len(emps__sec1) == 0:
        counts__1 = ""
        counttls1_emp = ""
        prs1 = ""
        plas1 = ""
        
    else:
        counts__1 = names_sec1
        counttls1_emp = len(emps__sec1)
        prs1 = projs___1
        plas1 = plats___1
 
# =============================================

    counts___2 = Counter(app__prosce2)
    ress2 = []
    for i in app__prosce2:
        if i not in ress2:
            ress2.append(i)
    resst2 = ress2
    projs___2 = []
    plats___2 = []

    for color2 in resst2:
         project = color2
         projs___2.append(project)
         Platform = counts___2[color2]
         plats___2.append(Platform)

    if len(emps__sec2) == 0:
        counts__2 = ""
        counttls2_emp = ""
        prs2 = ""
        plas2 = ""
        
    else:
        counts__2 = names_sec2
        counttls2_emp = len(emps__sec2)
        prs2 = projs___2
        plas2 = plats___2

  #================================================ 
    counts___3 = Counter(app__prosce3)
    ress3 = []
    for i in app__prosce3:
        if i not in ress3:
            ress3.append(i)
    resst3 = ress3
    projs___3 = []
    plats___3 = []

    for color3 in resst3:
         project = color3
         projs___3.append(project)
         Platform = counts___3[color3]
         plats___3.append(Platform)

    if len(emps__sec3) == 0:
        counts__3 = ""
        counttls3_emp = ""
        prs3 = ""
        plas3 = ""
        
    else:
        counts__3 = names_sec3
        counttls3_emp = len(emps__sec3)
        prs3 = projs___3
        plas3 = plats___3

# ========================================================================

    counts___4 = Counter(app__prosce4)
    ress4 = []
    for i in app__prosce4:
        if i not in ress4:
            ress4.append(i)
    resst4 = ress4
    projs___4 = []
    plats___4 = []

    for color4 in resst4:
         project = color4
         projs___4.append(project)
         Platform = counts___4[color4]
         plats___4.append(Platform)

    if len(emps__sec4) == 0:
        counts__4 = ""
        counttls4_emp = ""
        prs4 = ""
        plas4 = ""
        
    else:
        counts__4 = names_sec4
        counttls4_emp = len(emps__sec4)
        prs4 = projs___4
        plas4 = plats___4


# =========================================================================
    counts___5 = Counter(app__prosce5)
    ress5 = []
    for i in app__prosce5:
        if i not in ress5:
            ress5.append(i)
    resst5 = ress5
    projs___5 = []
    plats___5 = []

    for color5 in resst5:
         project = color5
         projs___5.append(project)
         Platform = counts___5[color5]
         plats___5.append(Platform)

    if len(emps__sec5) == 0:
        counts__5 = ""
        counttls5_emp = ""
        prs5 = ""
        plas5 = ""
        
    else:
        counts__5 = names_sec5
        counttls5_emp = len(emps__sec5)
        prs5 = projs___5
        plas5 = plats___5  



        
# ===================================================

    counts___6 = Counter(app__prosce6)
    ress6 = []
    for i in app__prosce6:
        if i not in ress6:
            ress6.append(i)
    resst6 = ress6
    projs___6 = []
    plats___6 = []

    for color6 in resst6:
         project = color6
         projs___6.append(project)
         Platform = counts___6[color6]
         plats___6.append(Platform)

    if len(emps__sec6) == 0:
        counts__6 = ""
        counttls6_emp = ""
        prs6 = ""
        plas6 = ""
        
    else:
        counts__6 = names_sec6
        counttls6_emp = len(emps__sec6)
        prs6 = projs___6
        plas6 = plats___6  

# ====================================================

    counts___7 = Counter(app__prosce7)
    ress7 = []
    for i in app__prosce7:
        if i not in ress7:
            ress7.append(i)
    resst7 = ress7
    projs___7 = []
    plats___7 = []

    for color7 in resst7:
         project = color7
         projs___7.append(project)
         Platform = counts___7[color7]
         plats___7.append(Platform)

    if len(emps__sec7) == 0:
        counts__7 = ""
        counttls7_emp = ""
        prs7 = ""
        plas7 = ""
        
    else:
        counts__7 = names_sec7
        counttls7_emp = len(emps__sec7)
        prs7 = projs___7
        plas7 = plats___7 

# ================================================
    counts___8 = Counter(app__prosce8)
    ress8 = []
    for i in app__prosce8:
        if i not in ress8:
            ress8.append(i)
    resst8 = ress8
    projs___8 = []
    plats___8 = []

    for color8 in resst8:
         project = color8
         projs___8.append(project)
         Platform = counts___8[color8]
         plats___8.append(Platform)

    if len(emps__sec8) == 0:
        counts__8 = ""
        counttls8_emp = ""
        prs8 = ""
        plas8 = ""
        
    else:
        counts__8 = names_sec8
        counttls8_emp = len(emps__sec8)
        prs8 = projs___8
        plas8 = plats___8

# ==================================================

    counts___9 = Counter(app__prosce9)
    ress9 = []
    for i in app__prosce9:
        if i not in ress9:
            ress9.append(i)
    resst9 = ress9
    projs___9 = []
    plats___9 = []

    for color9 in resst9:
         project = color9
         projs___9.append(project)
         Platform = counts___9[color9]
         plats___9.append(Platform)

    if len(emps__sec9) == 0:
        counts__9 = ""
        counttls9_emp = ""
        prs9 = ""
        plas9 = ""
        
    else:
        counts__9 = names_sec9
        counttls9_emp = len(emps__sec9)
        prs9 = projs___9
        plas9 = plats___9          


# ==================================================

    counts___10 = Counter(app__prosce10)
    ress10 = []
    for i in app__prosce10:
        if i not in ress10:
            ress10.append(i)
    resst10 = ress10
    projs___10 = []
    plats___10 = []

    for color10 in resst10:
         project = color10
         projs___10.append(project)
         Platform = counts___10[color10]
         plats___10.append(Platform)

    if len(emps__sec10) == 0:
        counts__10 = ""
        counttls10_emp = ""
        prs10 = ""
        plas10 = ""
        
    else:
        counts__10 = names_sec10
        counttls10_emp = len(emps__sec10)
        prs10 = projs___10
        plas10 = plats___10


# ==================================================

    counts___11 = Counter(app__prosce11)
    ress11 = []
    for i in app__prosce11:
        if i not in ress11:
            ress11.append(i)
    resst11 = ress11
    projs___11 = []
    plats___11 = []

    for color11 in resst11:
         project = color11
         projs___11.append(project)
         Platform = counts___11[color11]
         plats___11.append(Platform)

    if len(emps__sec11) == 0:
        counts__11 = ""
        counttls11_emp = ""
        prs11 = ""
        plas11 = ""
        
    else:
        counts__11 = names_sec11
        counttls11_emp = len(emps__sec11)
        prs11 = projs___11
        plas11 = plats___11

# ==================================================

    counts___12 = Counter(app__prosce12)
    ress12 = []
    for i in app__prosce12:
        if i not in ress12:
            ress12.append(i)
    resst12 = ress12
    projs___12 = []
    plats___12 = []

    for color12 in resst12:
         project = color12
         projs___12.append(project)
         Platform = counts___12[color12]
         plats___12.append(Platform)

    if len(emps__sec12) == 0:
        counts__12 = ""
        counttls12_emp = ""
        prs12 = ""
        plas12 = ""
        
    else:
        counts__12 = names_sec12
        counttls12_emp = len(emps__sec12)
        prs12 = projs___12
        plas12 = plats___12                    

# ==================================================

    counts___13 = Counter(app__prosce13)
    ress13 = []
    for i in app__prosce13:
        if i not in ress13:
            ress13.append(i)
    resst13 = ress13
    projs___13 = []
    plats___13 = []

    for color13 in resst13:
         project = color13
         projs___13.append(project)
         Platform = counts___13[color13]
         plats___13.append(Platform)

    if len(emps__sec13) == 0:
        counts__13 = ""
        counttls13_emp = ""
        prs13 = ""
        plas13 = ""
        
    else:
        counts__13 = names_sec13
        counttls13_emp = len(emps__sec13)
        prs13 = projs___13
        plas13 = plats___13                  



#============================/second======================






    

    

    counts__1 = Counter(app__projs1)
    res = []
    for i in app__projs1:
        if i not in res:
            res.append(i)
    rest1 = res
    proj___1 = []
    plat___1 = []

    for color1 in rest1:
         project = color1
         proj___1.append(project)
         Platform = counts__1[color1]
         plat___1.append(Platform)

    if len(emps__nsids1) == 0:
        count__1 = ""
        counttl1_emp = ""
        pr1 = ""
        pla1 = ""
        
    else:
        count__1 = names
        counttl1_emp = len(emps__nsids1)
        pr1 = proj___1
        pla1 = plat___1
 
# =============================================

    counts__2 = Counter(app__projs2)
    res1 = []
    for j in app__projs2:
        if j not in res1:
            res1.append(j)
    rest2 = res1
    proj___2 = []
    plat___2 = []
    for color2 in rest2:
         project2 = color2
         proj___2.append(project2)
         Platform2 = counts__2[color2]
         plat___2.append(Platform2)

    if len(emps__nsid2) == 0:
        count__2 = ""
        counttl2_emp = ""
        pr2 = ""
        pla2 = ""
    else:
        count__2 = names_2s
        counttl2_emp = len(emps__nsid2)
        pr2 = proj___2
        pla2 = plat___2

  #================================================ 
    counts__3 = Counter(app__projs3)
    res2 = []
    for k in app__projs3:
        if k not in res2:
            res2.append(k)
    rest3 = res2
    proj___3 = []
    plat___3 = []
    for color3 in rest3:
         project3 = color3
         proj___3.append(project3)
         Platform3 = counts__3[color3]
         plat___3.append(Platform3)

    if len(emps__nsid3) == 0:
        count__3 = ""
        counttl3_emp = ""
        pr3 = ""
        pla3 = ""
    else:
        count__3 = names_3s
        counttl3_emp = len(emps__nsid3)
        pr3 = proj___3
        pla3 = plat___3

# ========================================================================

    counts__4 = Counter(app__projs4)
    res3 = []
    for l in app__projs4:
        if l not in res3:
            res3.append(l)
    rest4 = res3
    proj___4 = []
    plat___4 = []
    for color4 in rest4:
         project4 = color4
         proj___4.append(project4)
         Platform4 = counts__4[color4]
         plat___4.append(Platform4)

    if len(emps__nsid4) == 0:
        count__4 = ""
        counttl4_emp = ""
        pr4 = ""
        pla4 = ""
    else:
        count__4 = names_4s
        counttl4_emp = len(emps__nsid4)
        pr4 = proj___4
        pla4 = plat___4


# =========================================================================
    counts__5 = Counter(app__projs5)
    res4 = []
    for m in app__projs5:
        if m not in res4:
            res4.append(m)
    rest5 = res4
    proj___5 = []
    plat___5 = []
    for color5 in rest5:
         project5 = color5
         proj___5.append(project5)
         Platform5 = counts__5[color5]
         plat___5.append(Platform5)

    if len(emps__nsid5) == 0:
        count__5 = ""
        counttl5_emp = ""
        pr5 = ""
        pla5 = ""
    else:
        count__5 = names_5s
        counttl5_emp = len(emps__nsid5)
        pr5 = proj___5
        pla5 = plat___5  



        
# ===================================================

    counts__6 = Counter(app__projs6)
    res5 = []
    for n in app__projs6:
        if n not in res5:
            res5.append(n)
    rest6 = res5
    proj___6 = []
    plat___6 = []
    for color6 in rest6:
         project6 = color6
         proj___6.append(project6)
         Platform6 = counts__6[color6]
         plat___6.append(Platform6)

    if len(emps__nsid6) == 0:
        count__6 = ""
        counttl6_emp = ""
        pr6 = ""
        pla6 = ""
    else:
        count__6 = names_6s
        counttl6_emp = len(emps__nsid6)
        pr6 = proj___6
        pla6 = plat___6  

# ====================================================

    counts__7 = Counter(app__projs7)
    res6 = []
    for o in app__projs7:
        if o not in res6:
            res6.append(o)
    rest7 = res6
    proj___7 = []
    plat___7 = []
    for color7 in rest7:
         project7 = color7
         proj___7.append(project7)
         Platform7 = counts__7[color7]
         plat___7.append(Platform7)

    if len(emps__nsid7) == 0:
        count__7 = ""
        counttl7_emp = ""
        pr7 = ""
        pla7 = ""
    else:
        count__7 = names_7s
        counttl7_emp = len(emps__nsid7)
        pr7 = proj___7
        pla7 = plat___7 

# ================================================
    counts__8 = Counter(app__projs8)
    res7 = []
    for p in app__projs8:
        if p not in res7:
            res7.append(p)
    rest8 = res7
    proj___8 = []
    plat___8 = []
    for color8 in rest8:
         project8 = color8
         proj___8.append(project8)
         Platform8 = counts__8[color8]
         plat___8.append(Platform8)

    if len(emps__nsid8) == 0:
        count__8 = ""
        counttl8_emp = ""
        pr8 = ""
        pla8 = ""
    else:
        count__8 = names_8s
        counttl8_emp = len(emps__nsid8)
        pr8 = proj___8
        pla8 = plat___8

# ==================================================

    counts__9 = Counter(app__projs9)
    res8 = []
    for q in app__projs9:
        if q not in res8:
            res8.append(q)
    rest9 = res8
    proj___9 = []
    plat___9 = []
    for color9 in rest9:
         project9 = color9
         proj___9.append(project9)
         Platform9 = counts__9[color9]
         plat___9.append(Platform9)

    if len(emps__nsid9) == 0:
        count__9 = ""
        counttl9_emp = ""
        pr9 = ""
        pla9 = ""
    else:
        count__9 = names_9s
        counttl9_emp = len(emps__nsid9)
        pr9 = proj___9
        pla9 = plat___9          


# ==================================================

    counts__10 = Counter(app__projs10)
    res9 = []
    for r in app__projs10:
        if r not in res9:
            res9.append(r)
    rest10 = res9
    proj___10 = []
    plat___10 = []
    for color10 in rest10:
         project10 = color10
         proj___10.append(project10)
         Platform10 = counts__10[color10]
         plat___10.append(Platform10)

    if len(emps__nsid10) == 0:
        count__10 = ""
        counttl10_emp = ""
        pr10 = ""
        pla10 = ""
    else:
        count__10 = names_10s
        counttl10_emp = len(emps__nsid10)
        pr10 = proj___10
        pla10 = plat___10


# ==================================================

    counts__11 = Counter(app__projs11)
    # print(counts__11)
    # exit()
    res10= []
    for s in app__projs11:
        if s not in res10:
            res10.append(s)
    rest11 = res10
    proj___11 = []
    plat___11 = []
    for color11 in rest11:
         project11 = color11
         proj___11.append(project11)
         Platform11 = counts__11[color11]
         plat___11.append(Platform11)

    if len(emps__nsid11) == 0:
        count__11 = ""
        counttl11_emp = ""
        pr11 = ""
        pla11 = ""
    else:
        count__11 = names_11s
        counttl11_emp = len(emps__nsid11)
        pr11 = proj___11
        pla11 = plat___11

# ==================================================

    counts__12 = Counter(app__projs12)
    res11= []
    for t in app__projs12:
        if t not in res11:
            res11.append(t)
    rest12 = res11
    proj___12 = []
    plat___12 = []
    for color12 in rest12:
         project12 = color12
         proj___12.append(project12)
         Platform12 = counts__12[color12]
         plat___12.append(Platform12)

    if len(emps__nsid12) == 0:
        count__12 = ""
        counttl12_emp = ""
        pr12 = ""
        pla12 = ""
    else:
        count__12 = names_12s
        counttl12_emp = len(emps__nsid12)
        pr12 = proj___12
        pla12 = plat___12                    

# ==================================================

    counts__13 = Counter(app__projs13)
    res12= []
    for u in app__projs13:
        if u not in res12:
            res12.append(u)
    rest13 = res12
    proj___13 = []
    plat___13 = []
    for color13 in rest13:
         project13 = color13
         proj___13.append(project13)
         Platform13 = counts__13[color13]
         plat___13.append(Platform13)

    if len(emps__nsid13) == 0:
        count__13 = ""
        counttl13_emp = ""
        pr13 = ""
        pla13 = ""
    else:
        count__13 = names_13s
        counttl13_emp = len(emps__nsid13)
        pr13 = proj___13
        pla13 = plat___13 



    #main datasds --------------------------------exit--------------------
    
    # print(counttl1_emp)
    print("====================================")
    # print(counttls1_emp)
    # exit()


    if counttl1_emp != '' and counttls1_emp == '':
        
        main_count1 = counttl1_emp

    else:
        
        main_count1 = counttl1_emp + counttls1_emp

        

    if counttl2_emp != '' and counttls2_emp == '':
        # main_count2 = counttl2_emp + counttls2_emp
        main_count2 = counttl2_emp
    else:
        main_count2 = counttl2_emp + counttls2_emp

    if counttl3_emp != '' and counttls3_emp == '':
        # main_count3 = counttl3_emp + counttls3_emp
        main_count3 = counttl3_emp
    else:
        main_count3 = counttl3_emp + counttls3_emp
        
    if counttl4_emp != '' and counttls4_emp == '':
        # main_count4 = counttl4_emp + counttls4_emp
        main_count4 = counttl4_emp
    else:
        main_count4 = counttl4_emp + counttls4_emp
        

    if counttl5_emp != '' and counttls5_emp == '':
        # main_count5 = counttl5_emp + counttls5_emp
        main_count5 = counttl5_emp
    else:
        main_count5 = counttl5_emp + counttls5_emp
        
    if counttl6_emp != '' and counttls6_emp == '':
        # main_count6 = counttl6_emp + counttls6_emp
        main_count6 = counttl6_emp
    else:
        main_count6 = counttl6_emp + counttls6_emp
        

    if counttl7_emp != '' and counttls7_emp == '':
        # main_count7 = counttl7_emp + counttls7_emp
        main_count7 = counttl7_emp
    else:
        main_count7 = counttl7_emp + counttls7_emp
    
    if counttl8_emp != '' and counttls8_emp == '':
        # main_count8 = counttl8_emp + counttls8_emp
        main_count8 = counttl8_emp
    else:
        main_count8 = counttl8_emp + counttls8_emp

    if counttl9_emp != '' and counttls9_emp == '':
        # main_count9 = counttl9_emp + counttls9_emp
        main_count9 = counttl9_emp
    else:
        main_count9 = counttl9_emp + counttls9_emp
        
    if counttl10_emp != '' and counttls10_emp == '':
        # main_count10 = counttl10_emp + counttls10_emp
        main_count10 = counttl10_emp
    else:
        main_count10 = counttl10_emp + counttls10_emp
        

    if counttl11_emp != '' and counttls11_emp == '':
        # main_count11 = counttl11_emp + counttls11_emp
        main_count11 = counttl11_emp
    else:
        main_count11 = counttl11_emp + counttls11_emp                                       




    if counttl12_emp != '' and counttls12_emp == '':
        # main_count12 = counttl12_emp + counttls12_emp
        main_count12 = counttl12_emp
    else:
        main_count12 = counttl12_emp + counttls12_emp

    if counttl13_emp != '' and counttls13_emp == '':
        # main_count13 = counttl13_emp + counttls13_emp
        main_count13 = counttl13_emp
    else:
        main_count13 = counttl13_emp + counttls13_emp    
    #main--------datasd exit ---------------------------------------------    


    

    return render(request, "employee_register/overall_data.html",{'main_count1':main_count1,'main_count2':main_count2,'main_count4':main_count4,'main_count5':main_count5,'main_count6':main_count6,'main_count7':main_count7,'main_count8':main_count8,'main_count9':main_count9,'main_count10':main_count10,'main_count11':main_count11,'main_count12':main_count12,'main_count13':main_count13,'count__13':count__13,'counttl13_emp':counttl13_emp,'pr13':pr13,'pla13':pla13,'count__11':count__11,'counttl11_emp':counttl11_emp,'pr11':pr11,'pla11':pla11,'count__12':count__12,'counttl12_emp':counttl12_emp,'pr12':pr12,'pla12':pla12,'count__10':count__10,'counttl10_emp':counttl10_emp,'pr10':pr10,'pla10':pla10,'count__9':count__9,'counttl9_emp':counttl9_emp,'pr9':pr9,'pla9':pla9,'count__8':count__8,'counttl8_emp':counttl8_emp,'pr8':pr8,'pla8':pla8,'count__7':count__7,'counttl7_emp':counttl7_emp,'pr7':pr7,'pla7':pla7,'count__6':count__6,'counttl6_emp':counttl6_emp,'pr6':pr6,'pla6':pla6,'count__5':count__5,'counttl5_emp':counttl5_emp,'pr5':pr5,'pla5':pla5 ,'count__4':count__4,'counttl4_emp':counttl4_emp,'pr4':pr4,'pla4':pla4,'count__3':count__3,'counttl3_emp':counttl3_emp,'pr3':pr3,'pla3':pla3,'count__2':count__2,'counttl2_emp':counttl2_emp,'pr2':pr2,'pla2':pla2,'date':split_daten,'count__1':count__1,'counttl1_emp':counttl1_emp,'pr1':pr1,'pla1':pla1,'counttl1_emp':counttl1_emp,'counts_people':counts_people,'counts__1':counts__1,'counttls1_emp':counttls1_emp,'prs1':prs1,'plas1':plas1,'counts__2':counts__2,'counttls2_emp':counttls2_emp,'prs2':prs2,'plas2':plas2,'counts__3':counts__3,'counttls3_emp':counttls3_emp,'prs3':prs3,'plas3':plas3,'counts__4':counts__4,'counttls4_emp':counttls4_emp,'prs4':prs4,'plas4':plas4,'counts__5':counts__5,'counttls5_emp':counttls5_emp,'prs5':prs5,'plas5':plas5,'counts__6':counts__6,'counttls6_emp':counttls6_emp,'prs6':prs6,'plas6':plas6,'counts__7':counts__7,'counttls7_emp':counttls7_emp,'prs7':prs7,'plas7':plas7,'counts__8':counts__8,'counttls8_emp':counttls8_emp,'prs8':prs8,'plas8':plas8,'counts__9':counts__9,'counttls9_emp':counttls9_emp,'prs9':prs9,'plas9':plas9,'counts__10':counts__10,'counttls10_emp':counttls10_emp,'prs10':prs10,'plas10':plas10,'counts__11':counts__11,'counttls11_emp':counttls11_emp,'prs11':prs11,'plas11':plas11,'counts__12':counts__12,'counttls12_emp':counttls12_emp,'prs12':prs12,'plas12':plas12,'counts__13':counts__13,'counttls13_emp':counttls13_emp,'prs13':prs13,'plas13':plas13,'main_count3':main_count3})
 
        

        






        



        

  


# 'counts__1':counts__1,'counttls1_emp':counttls1_emp,'prs1':prs1,'plas1':plas1,
# 'counts__2':counts__2,'counttls2_emp':counttls2_emp,'prs2':prs2,'plas2':plas2,
# 'counts__3':counts__3,'counttls3_emp':counttls3_emp,'prs3':prs3,'plas3':plas3,
# 'counts__4':counts__4,'counttls4_emp':counttls4_emp,'prs4':prs4,'plas4':plas4,
# 'counts__5':counts__5,'counttls5_emp':counttls5_emp,'prs5':prs5,'plas5':plas5,
# 'counts__6':counts__6,'counttls6_emp':counttls6_emp,'prs6':prs6,'plas6':plas6,
# 'counts__7':counts__7,'counttls7_emp':counttls7_emp,'prs7':prs7,'plas7':plas7,
# 'counts__8':counts__8,'counttls8_emp':counttls8_emp,'prs8':prs8,'plas8':plas8,
# 'counts__9':counts__9,'counttls9_emp':counttls9_emp,'prs9':prs9,'plas9':plas9,
# 'counts__10':counts__10,'counttls10_emp':counttls10_emp,'prs10':prs10,'plas10':plas10,
# 'counts__11':counts__11,'counttls11_emp':counttls11_emp,'prs11':prs11,'plas11':plas11,
# 'counts__12':counts__12,'counttls12_emp':counttls12_emp,'prs12':prs12,'plas12':plas12,
# 'counts__13':counts__13,'counttls13_emp':counttls13_emp,'prs13':prs13,'plas13':plas13,

        
         




    # if len(emps__nsids1) == 0:
        
        
    # else:
    #     count__1 = names
    #     counttl1_emp = len(emps__nsids1)
    #     counttl1_1 = Counter(app__projs1)

    
    # if len(emps__nsid2) == 0:
    #     count2 = ""
    #     counttl2_emp = ""
    #     counttl2_2 = ""
    # else:
    #     count2 = names_2s
    #     counttl2_emp = len(emps__nsid2)
    #     counttl2_2 = Counter(app__projs2)
            

    
    # if len(emps__nsid3) == 0:
    #     count3 = ''
    #     counttl3_emp = ""
    #     counttl3_3 = ""
        
    # else:
    #     count3 = names_3s
    #     counttl3_emp = len(emps__nsid3)
    #     counttl3_3 = Counter(app__projs3)

    
    # if len(emps__nsid4) == 0:
    #     count4 = ''
    #     counttl4_emp = ""
    #     counttl4_4 = ""
    # else:
    #     count4 = names_4s
    #     counttl4_emp = len(emps__nsid4)
    #     counttl4_4 = Counter(app__projs4)

    

    # if len(emps__nsid5) == 0:
    #     count5 = ''
    #     counttl5_emp = ""
    #     counttl5_5 = ""
    # else:
    #     count5 = names_5s
    #     counttl5_emp = len(emps__nsid5)
    #     counttl5_5 = Counter(app__projs5)


    
    # if len(emps__nsid6) == 0:
    #     count6 = ''
    #     counttl6_emp = ""
    #     counttl6_6 = ""
    # else:
    #     count6 = names_6s
    #     counttl6_emp = len(emps__nsid6)
    #     counttl6_6 = Counter(app__projs6)



    # if len(emps__nsid7) == 0:
    #     count7 = ''
    #     counttl7_emp = ""
    #     counttl7_7 = ""
    # else:
    #     count7 = names_7s
    #     counttl7_emp = len(emps__nsid7)
    #     counttl7_7 = Counter(app__projs7)

    # if len(emps__nsid8) == 0:
    #     count8 = ''
    #     counttl8_emp = ""
    #     counttl8_8 = ""
    # else:
    #     count8 = names_8s
    #     counttl8_emp = len(emps__nsid8)
    #     counttl8_8 = Counter(app__projs8)
    # if len(emps__nsid8) == 0:
    #     count9 = ''
    #     counttl9_emp = ""
    #     counttl9_9 = ""
    # else:
    #     count9 = names_9s
    #     counttl9_emp = len(emps__nsid9)
    #     counttl9_9 = Counter(app__projs9)

    # if len(emps__nsid10) == 0:
    #     count10 = ''
    #     counttl10_emp = ""
    #     counttl10_10 = ""
    # else:
    #     count10 = names_10s
    #     counttl10_emp = len(emps__nsid10)
    #     counttl10_10 = Counter(app__projs10)


    # if len(emps__nsid11) == 0:
    #     count11 = ''
    #     counttl11_emp = ""
    #     counttl11_11 = ""
    # else:
    #     count11 = names_11s
    #     counttl11_emp = len(emps__nsid11)
    #     counttl11_11 = Counter(app__projs11)
        

    # if len(emps__nsid12) == 0:
    #     count12 = ''
    #     counttl12_emp = ""
    #     counttl12_12 = ""
    # else:
    #     count12 = names_12s
    #     counttl12_emp = len(emps__nsid12)
    #     counttl12_12 = Counter(app__projs12)                 


    # return render(request, "employee_register/overall_data.html",{'date':split_daten,'count__1':count__1,'counttl7_emp':counttl7_emp,'counttl7_7':counttl7_7, 'counttl1_emp':counttl1_emp, 'counttl1_1':counttl1_1, 'count2':count2, 'counttl2_emp':counttl2_emp,'counttl2_2':counttl2_2,'count7':count7,'count3':count3,'count4':count4,'count5':count5,'count6':count6,'count8':count8,'count9':count9,'count10':count10,'counttl3_emp':counttl3_emp,'counttl4_emp':counttl4_emp,'counttl5_emp':counttl5_emp,'counttl6_emp':counttl6_emp,'counttl8_emp':counttl8_emp,'counttl9_emp':counttl9_emp,'counttl10_emp':counttl10_emp,'counttl3_3':counttl3_3,'counttl4_4':counttl4_4,'counttl5_5':counttl5_5,'counttl6_6':counttl6_6,'counttl8_8':counttl8_8,'counttl9_9':counttl9_9,'counttl10_10':counttl10_10,'count11':count11,'count12':count12,'counttl11_emp':counttl11_emp,'counttl12_emp':counttl12_emp,'counttl11_11':counttl11_11,'counttl12_12':counttl12_12,'counts_people':counts_people})

     
    
    
    

    





    



    

  
    


        
    
 
    

            # if form.is_valid():
            #     form.save()
                

            #     fulln = form.cleaned_data['full_name']
            #     mob = form.cleaned_data['mobile']
            #     proj = form.cleaned_data['projects']
            #     platf = form.cleaned_data['platform']
        # form = EmployeeInserForm()

        
        
            
        
    # print("here")
    # exit()





# https://www.youtube.com/watch?v=JVFH8fuR4l0
# https://www.youtube.com/watch?v=JVFH8fuR4l0

# https://www.youtube.com/watch?v=qSjSn620vhI
# Newparts

# chmod 400 ec2_key.pem        

# ssh -i "akash_e2c_key.pem" ubuntu@ec2-52-22-227-158.compute-1.amazonaws.com


# CREATE USER 'root'@'%' IDENTIFIED BY 'root';
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

# sudo apt-get update

# sudo apt-get install php-fpm php-mysqlhttps://github.com/AkashAnoly-uk/employee/commits?author=AkashAnoly-uk

# sudo apt install mysql-server

# sudo /etc/init.d/apache2 restart

# sudo service apache2 status
# sudo apt-get install php-fpm php-mysql
# sudo apt-get install phpmyadmin
# sudo apt-get install libapache2-mod-php
# sudo ln -s /usr/share/phpmyadmin /var/www/html
# sudo systemctl restart nginx

# sudo nano /etc/nginx/sites-available/default
# sudo systemctl reload nginx
# sudo ln -s /usr/share/phpmyadmin /var/www/html


# CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';

# rm -r akashemps


# sudo apt install git-all
# FLUSH PRIVILEGES;



# sudo ln -s /usr/share/phpmyadmin /var/www/52.22.227.158/phpmyadmin

# https://stackoverflow.com/questions/68775869/support-for-password-authentication-was-removed-please-use-a-personal-access-to

# github_token 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

# git remote add origin ssh://git@github.com:AkashAnoly-uk/employee.git

# git remote set-url origin https://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@github.com/AkashAnoly-uk/employee.git

# git@github.com:AkashAnoly-uk/employee.git

# git remote set-url origin https://github.com/AkashAnoly-uk/employee.git
                            # https://github.com/AkashAnoly-uk/employee

# git remote set-url origin https://scuzzlebuzzle:<MYTOKEN>@github.com/scuzzlebuzzle/ol3-1.git

# git remote set-url origin ssh://git@github.com:AkashAnoly-uk/akshrepos.git



                            # git remote add origin ssh://github.com/AkashAnoly-uk/akashemps
                            # git remote add origin ssh://github.com:AkashAnoly-uk/akshrepos.git
                            # git clone git@github.com:AkashAnoly-uk/akashemps.git
                            # git clone git@github.com:AkashAnoly-uk/employee.git
                            # git clone git@github.com:Utshuk/Django.git


                            # git remote add origin ssh://github.com/AkashAnoly-uk/akashemps

                            # git remote add origin ssh://git@github.com:AkashAnoly-uk/employee.git


                            # git clone https://github.com/AkashAnoly-uk/employee.git
                           #  https://github.com/AkashAnoly-uk/employee.git
                           # git clone https://github.com/AkashAnoly-uk/employee/tree/master

                            # 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

                            # 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  akashDjango new tokkens\

                            # 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 final token

# sudo mysql -p -u root

# CREATE USER 'USERNAME'@'%' IDENTIFIED BY 'PASSWORD';
# GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'%' WITH GRANT OPTION;

# sudo mysql -u root;
# use mysql;
# UPDATE mysql.user SET plugin = 'mysql_native_password', Password = PASSWORD('pass1234') WHERE User = 'root';
# FLUSH PRIVILEGES;
# exit;


# UPDATE user SET Password='root' WHERE User='root'; FLUSH PRIVILEGES; exit;


   




    



            
  


    


                

        

    
   





               

        

    

    




    





