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


        
        return render(request, "employee_register/project_form.html")
  

   
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

  

        return render(request, "employee_register/project_form.html")



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
    # return render(request, "employee_register/reassign_user.html")
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

        # print(new_app)
        # exit()

 
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

        # print(new_ints)
        # exit()    

   

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)

        new_apend_data = [] 

        # difference = set(new_app).symmetric_difference(set(new_ints))
        # list_difference = list(difference)
        # count_person = len(list_difference)
 
 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=new_ints)

 
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
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)


                # survey = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)

                ckeck = assignment.objects.filter(date_from__gte=today_min).filter(employeeid=item).exclude(first_work_done__isnull=True).exclude(first_work_done__exact='')
                
                
                    

                ckeck1 = assignment.objects.filter(from_to__gte=today_min).filter(employeeid=item).filter(first_work_done=' ')
                

                if ckeck.count() == 0:
                    print("Yes")
                    update = assignment.objects.filter(employeeid= item).filter(date_from__gte=today_min).update(first_work_done='Done')
                    survey = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)
                else:

                    if ckeck1.count() == 0:
                        print("same")
                        assignment.objects.filter(employeeid= item).filter(from_to__gte=today_min).update(first_work_done='Done')
                        survey = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)
                    
      
                
            
            return render(request, "employee_register/assigned.html")        




            
            

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
    assignment1 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl1_ids)

    empidap =[]
    projap = []
    tls_part = []

    for upd_status in assignment1:
        
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
    assignment2 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl1_ids1)

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
    assignment2 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl2_ids2)

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
    assignment3 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl3_ids3)

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
    # assigned = assignment.objects.filter(first_work_done='Done').filter(date_from__gte=today_min)
    # assignmentnew = assignment.objects.filter(from_to__gte=today_min).filter(tl_id=tl4_ids4)

    # print(assignment4)
    # exit()

    
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
    assignment4 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl4_ids4)

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
    assignment5 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl5_ids5)

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
    assignment6 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl6_ids6)

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
    assignment7 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl7_ids7)

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
    assignment8 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl8_ids8)

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
    assignment9 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl9_ids9)

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
    assignment10 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl10_ids10)

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

    # print(assign)
    # exit()

    
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
    assignment11 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl11_ids11)


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
    assignment12 = assignment.objects.filter(from_to__gte=today_min).filter(first_work_done='').filter(tl_id=tl12_ids12)

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
    



    return render(request, "employee_register/assigned.html",{'emp_det_id12':emp_det_id12,'new_app12':new_app12,'new_prj12':new_prj12,'tl_fulname12':tl_fulname12,'ressignm_det12':ressignm_det12,'se_proj12':se_proj12,'se_plat12':se_plat12,'tl__fulname12':tl__fulname12,'emp_det_id11':emp_det_id11,'new_app11':new_app11,'new_prj11':new_prj11,'tl_fulname11':tl_fulname11,'ressignm_det11':ressignm_det11,'se_proj11':se_proj11,'se_plat11':se_plat11,'tl__fulname11':tl__fulname11,'emp_det_id10':emp_det_id10,'new_app10':new_app10,'new_prj10':new_prj10,'tl_fulname10':tl_fulname10,'ressignm_det10':ressignm_det10,'se_proj10':se_proj10,'se_plat10':se_plat10,'tl__fulname10':tl__fulname10,'emp_det_id9':emp_det_id9,'new_app9':new_app9,'new_prj9':new_prj9,'tl_fulname9':tl_fulname9,'ressignm_det9':ressignm_det9,'se_proj9':se_proj9,'se_plat9':se_plat9,'tl__fulname9':tl__fulname9,'emp_det_id8':emp_det_id8,'new_app8':new_app8,'new_prj8':new_prj8,'tl_fulname8':tl_fulname8,'ressignm_det8':ressignm_det8,'se_proj8':se_proj8,'se_plat8':se_plat8,'tl__fulname8':tl__fulname8,'emp_det_id7':emp_det_id7,'new_app7':new_app7,'new_prj7':new_prj7,'tl_fulname7':tl_fulname7,'ressignm_det7':ressignm_det7,'se_proj7':se_proj7,'se_plat7':se_plat7,'tl__fulname7':tl__fulname7,'emp_det_id6':emp_det_id6,'new_app6':new_app6,'new_prj6':new_prj6,'tl_fulname6':tl_fulname6,'ressignm_det6':ressignm_det6,'se_proj6':se_proj6,'se_plat6':se_plat6,'tl__fulname6':tl__fulname6,'emp_det_id5':emp_det_id5,'new_app5':new_app5,'new_prj5':new_prj5,'tl_fulname5':tl_fulname5,'ressignm_det5':ressignm_det5,'se_proj5':se_proj5,'se_plat5':se_plat5,'tl__fulname5':tl__fulname5,'emp_det_id4':emp_det_id4,'new_app4':new_app4,'new_prj4':new_prj4,'tl_fulname4':tl_fulname4,'ressignm_det4':ressignm_det4,'se_proj4':se_proj4,'se_plat4':se_plat4,'tl__fulname4':tl__fulname4,'emp_det_id3':emp_det_id3,'new_app3':new_app3,'new_prj3':new_prj3,'tl_fulname3':tl_fulname3,'ressignm_det3':ressignm_det3,'se_proj3':se_proj3,'se_plat3':se_plat3,'tl__fulname3':tl__fulname3,'emp_det_id2':emp_det_id2,'new_app2':new_app2,'new_prj2':new_prj2,'tl_fulname2':tl_fulname2,'ressignm_det2':ressignm_det2,'se_proj2':se_proj2,'se_plat2':se_plat2,'tl__fulname2':tl__fulname2,'emp_det_id1':emp_det_id1,'new_app1':new_app1,'new_prj1':new_prj1,'tl_fulname1':tl_fulname1,'ressignm_det1':ressignm_det1,'se_proj1':se_proj1,'se_plat1':se_plat1,'tl__fulname1':tl__fulname1,'emp_det':emp_det_id,'proj_name':new_app,'pla_name':new_prj,'ressignm_det':ressignm_det,'se_proj':se_proj,'se_plat':se_plat,'date':split_daten, 'tl_fulname':tl_fulname,'tl__fulname':tl__fulname, 'counts_ass':counts_ass})            






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






    

    

    countes__1 = Counter(app__projs1)
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
         Platform = countes__1[color1]
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

    countes__2 = Counter(app__projs2)
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
         Platform2 = countes__1[color2]
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
    countes__3 = Counter(app__projs3)
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
         Platform3 = countes__1[color3]
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

    countes__4 = Counter(app__projs4)
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
         Platform4 = countes__4[color4]
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
    countes__5 = Counter(app__projs5)
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
         Platform5 = countes__5[color5]
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

    countes__6 = Counter(app__projs6)
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
         Platform6 = countes__6[color6]
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

    countes__7 = Counter(app__projs7)
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
         Platform7 = countes__7[color7]
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
    countes__8 = Counter(app__projs8)
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
         Platform8 = countes__8[color8]
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

    countes__9 = Counter(app__projs9)
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
         Platform9 = countes__9[color9]
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

    countes__10 = Counter(app__projs10)
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
         Platform10 = countes__10[color10]
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

    countes__11 = Counter(app__projs11)
    # print(countes__11)
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
         Platform11 = countes__11[color11]
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

    countes__12 = Counter(app__projs12)
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
         Platform12 = countes__12[color12]
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

    countes__13 = Counter(app__projs13)
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
         Platform13 = countes__13[color13]
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
    
  
    print("====================================")




    if counttl1_emp == '':
        main_count1 = counttls1_emp
    elif counttls1_emp == '':
        main_count1 = counttl1_emp
    else:
        main_count1 = counttl1_emp + counttls1_emp

    
    if counttl2_emp == '':
        main_count2 = counttls2_emp
    elif counttls2_emp == '':
        main_count2 = counttl2_emp
    else:
        main_count2 = counttl2_emp + counttls2_emp

    if counttl3_emp == '':
        main_count3 = counttls3_emp
    elif counttls3_emp == '':
        main_count3 = counttl3_emp
    else:
        main_count3 = counttl3_emp + counttls3_emp    


    if counttl4_emp == '':
        main_count4 = counttls4_emp
    elif counttls4_emp == '':
        main_count4 = counttl4_emp
    else:
        main_count4 = counttl4_emp + counttls4_emp

    if counttl5_emp == '':
        main_count5 = counttls5_emp
    elif counttls5_emp == '':
        main_count5 = counttl5_emp
    else:
        main_count5 = counttl5_emp + counttls5_emp
        


    if counttl6_emp == '':
        main_count6 = counttls6_emp
    elif counttls6_emp == '':
        main_count6 = counttl6_emp
    else:
        main_count6 = counttl6_emp + counttls6_emp
    

    if counttl7_emp == '':
        main_count7 = counttls7_emp
    elif counttls7_emp == '':
        main_count7 = counttl7_emp
    else:
        main_count7 = counttl7_emp + counttls7_emp

    if counttl8_emp == '':
        main_count8 = counttls8_emp
    elif counttls8_emp == '':
        main_count8 = counttl8_emp
    else:
        main_count8 = counttl8_emp + counttls8_emp
        
    
    if counttl9_emp == '':
        main_count9 = counttls9_emp
    elif counttls9_emp == '':
        main_count9 = counttl9_emp
    else:
        main_count9 = counttl9_emp + counttls9_emp

    if counttl10_emp == '':
        main_count10 = counttls10_emp
    elif counttls10_emp == '':
        main_count10 = counttl10_emp
    else:
        main_count10 = counttl10_emp + counttls10_emp
        
    
    if counttl11_emp == '':
        main_count11 = counttls11_emp
    elif counttls11_emp == '':
        main_count11 = counttl11_emp
    else:
        main_count11 = counttl11_emp + counttls11_emp


    if counttl12_emp == '':
        main_count12 = counttls12_emp
    elif counttls12_emp == '':
        main_count12 = counttl12_emp
    else:
        main_count12 = counttl12_emp + counttls12_emp



    if counttl13_emp == '':
        main_count13 = counttls13_emp
    elif counttls13_emp == '':
        main_count13 = counttl13_emp
    else:
        main_count13 = counttl13_emp + counttls13_emp       



    return render(request, "employee_register/overall_data.html",{'main_count1':main_count1,'main_count2':main_count2,'main_count4':main_count4,'main_count5':main_count5,'main_count6':main_count6,'main_count7':main_count7,'main_count8':main_count8,'main_count9':main_count9,'main_count10':main_count10,'main_count11':main_count11,'main_count12':main_count12,'main_count13':main_count13,'count__13':count__13,'counttl13_emp':counttl13_emp,'pr13':pr13,'pla13':pla13,'count__11':count__11,'counttl11_emp':counttl11_emp,'pr11':pr11,'pla11':pla11,'count__12':count__12,'counttl12_emp':counttl12_emp,'pr12':pr12,'pla12':pla12,'count__10':count__10,'counttl10_emp':counttl10_emp,'pr10':pr10,'pla10':pla10,'count__9':count__9,'counttl9_emp':counttl9_emp,'pr9':pr9,'pla9':pla9,'count__8':count__8,'counttl8_emp':counttl8_emp,'pr8':pr8,'pla8':pla8,'count__7':count__7,'counttl7_emp':counttl7_emp,'pr7':pr7,'pla7':pla7,'count__6':count__6,'counttl6_emp':counttl6_emp,'pr6':pr6,'pla6':pla6,'count__5':count__5,'counttl5_emp':counttl5_emp,'pr5':pr5,'pla5':pla5 ,'count__4':count__4,'counttl4_emp':counttl4_emp,'pr4':pr4,'pla4':pla4,'count__3':count__3,'counttl3_emp':counttl3_emp,'pr3':pr3,'pla3':pla3,'count__2':count__2,'counttl2_emp':counttl2_emp,'pr2':pr2,'pla2':pla2,'date':split_daten,'count__1':count__1,'counttl1_emp':counttl1_emp,'pr1':pr1,'pla1':pla1,'counttl1_emp':counttl1_emp,'counts_people':counts_people,'counts__1':counts__1,'counttls1_emp':counttls1_emp,'prs1':prs1,'plas1':plas1,'counts__2':counts__2,'counttls2_emp':counttls2_emp,'prs2':prs2,'plas2':plas2,'counts__3':counts__3,'counttls3_emp':counttls3_emp,'prs3':prs3,'plas3':plas3,'counts__4':counts__4,'counttls4_emp':counttls4_emp,'prs4':prs4,'plas4':plas4,'counts__5':counts__5,'counttls5_emp':counttls5_emp,'prs5':prs5,'plas5':plas5,'counts__6':counts__6,'counttls6_emp':counttls6_emp,'prs6':prs6,'plas6':plas6,'counts__7':counts__7,'counttls7_emp':counttls7_emp,'prs7':prs7,'plas7':plas7,'counts__8':counts__8,'counttls8_emp':counttls8_emp,'prs8':prs8,'plas8':plas8,'counts__9':counts__9,'counttls9_emp':counttls9_emp,'prs9':prs9,'plas9':plas9,'counts__10':counts__10,'counttls10_emp':counttls10_emp,'prs10':prs10,'plas10':plas10,'counts__11':counts__11,'counttls11_emp':counttls11_emp,'prs11':prs11,'plas11':plas11,'counts__12':counts__12,'counttls12_emp':counttls12_emp,'prs12':prs12,'plas12':plas12,'counts__13':counts__13,'counttls13_emp':counttls13_emp,'prs13':prs13,'plas13':plas13,'main_count3':main_count3})
 
        




    





