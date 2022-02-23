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

        if platname == 'none' and tl_id =='none':
            return HttpResponse('DROPDOWN NOT SELECTED')
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

        if platname == 'none' and tl_id =='none':
            return HttpResponse('DROPDOWN NOT SELECTED')
        else:
            for index, item in enumerate(recomme):
                new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                today1 = str(new_date)
                split_a = today1.split(".")
                split_date = split_a[0]
                split_date1 = str(split_date).split(" ")
                split_daten = split_date1[0]
                survey = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)
       

            return render(request, "employee_register/assigned.html")    


         
            


def assign_previous(request):
    if request.method == "GET":

        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]


         
        assign = assignment.objects.values_list('employeeid', flat=True)
        
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))
        

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))
      

        srt_paqtmax = str(today_max)
        split_partmax = srt_paqtmax.split(' ')
        split_partmax[0] = yesterday
        yesterday_max = " ".join(map(str,split_partmax))
   

        # ---------------------todays_task----start---------------------
       
        
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

        assign_today = assignment.objects.filter(date_from__gte=today_min)

        assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(date_from__lte=yesterday_max)
   
        proj_idds = []

        for update_s in assign_yestday:
            pro_ids = update_s.projectid
            proj_idds.append(pro_ids)

        pro_app= []

        for projs in proj_idds:
            pro_in = int(projs)
            pro_app.append(pro_in)

        empidappend = []

        for update_status in assign_today:
            empsids = update_status.employeeid
            empidappend.append(empsids)


        emptody_app= []

       
        for ints in empidappend:
            ints = int(ints)
            emptody_app.append(ints)
     
  

            # -------------------------------------------

        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active').filter(role="IA")
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)


        new_apend_data = [] 

        difference = set(emptody_app).symmetric_difference(set(apppend_id))
        list_difference = list(difference)

 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)

        return render(request, "employee_register/assign_previous.html",{ 'emp_proj':id_filter,'date':yesterday})

    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']

   
        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]    

        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
       
        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))

        if len(recomme) == 0:

            assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(projectid=platname)
            emy_id =[]
            for update_e in assign_yestday:
                empsids = update_e.employeeid
                emy_id.append(empsids)

            active_emp_yesterday = employee_details.objects.filter(pk__in=emy_id)

            

            active_emp_today = assignment.objects.filter(date_from__gte=today_min).filter(projectid=platname)
  
            emp_yest = []


            for stat_e in active_emp_yesterday:
                emp_ids = stat_e.id
                emp_yest.append(emp_ids)

            emptoday = []

            for stat_u in active_emp_today:
                emp_tody = stat_u.employeeid
                emptoday.append(emp_tody)
            
            emptoday_n = []    
            for ints in emptoday:
                ints = int(ints)
                emptoday_n.append(ints)
            
            difference = set(emp_yest).symmetric_difference(set(emptoday_n))
            list_difference = list(difference)
            emp_projs = projects.objects.filter(open_status__gte=today_min)
           
        
            new_updatestes = []
            for n_update in emp_projs:
                open_o = n_update.open_status 
                close_o = n_update.close_status
                if open_o and close_o == '':
                    open_d = n_update.id
                    new_updatestes.append(open_d)
                    
                else:
                    pass

            listsss =[platname]
        

                
            id_filter = projects.objects.filter(pk__in=listsss)
            active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
        

            active_emp = employee_details.objects.filter(pk__in=list_difference)
            platform_proj = projects.objects.filter(pk__in=listsss)
            

            return render(request, "employee_register/assign_previousdata.html",{'active_emp':active_emp,'active_tl':active_tl,'emp_proj':id_filter,'date':yesterday})
      
        else:
            if request.method == 'POST':

                recomme=request.POST.getlist('interest')
                platname = request.POST['options']
                tl_id = request.POST['option_tl']
            if platname == 'none' and tl_id =='none':
                return HttpResponse('DROPDOWN NOT SELECTED')
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
            
            
            



       
def assigned(request):
    new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today1 = str(new_date)
    split_a = today1.split(".")
    split_date = split_a[0]
    split_date1 = str(split_date).split(" ")
    split_daten = split_date1[0]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
 
    assign = assignment.objects.filter(date_from__gte=today_min)

    counts_ass = len(assign)

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
    assignment2 = assignment.objects.filter(from_to__gte=today_min)

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
        # print(piks)
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
    


    return render(request, "employee_register/assigned.html",{'emp_det':emp_det_id,'proj_name':new_app,'pla_name':new_prj,'ressignm_det':ressignm_det,'se_proj':se_proj,'se_plat':se_plat,'date':split_daten, 'tl_fulname':tl_fulname,'tl__fulname':tl__fulname, 'counts_ass':counts_ass})



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
    

    assigns__n = assignment.objects.filter(date_from__gte=today_min)

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



        
    return render(request, "employee_register/overall_data.html",{'count__13':count__13,'counttl13_emp':counttl13_emp,'pr13':pr13,'pla13':pla13,'count__11':count__11,'counttl11_emp':counttl11_emp,'pr11':pr11,'pla11':pla11,'count__12':count__12,'counttl12_emp':counttl12_emp,'pr12':pr12,'pla12':pla12,'count__10':count__10,'counttl10_emp':counttl10_emp,'pr10':pr10,'pla10':pla10,'count__9':count__9,'counttl9_emp':counttl9_emp,'pr9':pr9,'pla9':pla9,'count__8':count__8,'counttl8_emp':counttl8_emp,'pr8':pr8,'pla8':pla8,'count__7':count__7,'counttl7_emp':counttl7_emp,'pr7':pr7,'pla7':pla7,'count__6':count__6,'counttl6_emp':counttl6_emp,'pr6':pr6,'pla6':pla6,'count__5':count__5,'counttl5_emp':counttl5_emp,'pr5':pr5,'pla5':pla5 ,'count__4':count__4,'counttl4_emp':counttl4_emp,'pr4':pr4,'pla4':pla4,'count__3':count__3,'counttl3_emp':counttl3_emp,'pr3':pr3,'pla3':pla3,'count__2':count__2,'counttl2_emp':counttl2_emp,'pr2':pr2,'pla2':pla2,'date':split_daten,'count__1':count__1,'counttl1_emp':counttl1_emp,'pr1':pr1,'pla1':pla1,'counttl1_emp':counttl1_emp,'counts_people':counts_people,'counts__1':counts__1,'counttls1_emp':counttls1_emp,'prs1':prs1,'plas1':plas1,'counts__2':counts__2,'counttls2_emp':counttls2_emp,'prs2':prs2,'plas2':plas2,'counts__3':counts__3,'counttls3_emp':counttls3_emp,'prs3':prs3,'plas3':plas3,'counts__4':counts__4,'counttls4_emp':counttls4_emp,'prs4':prs4,'plas4':plas4,'counts__5':counts__5,'counttls5_emp':counttls5_emp,'prs5':prs5,'plas5':plas5,'counts__6':counts__6,'counttls6_emp':counttls6_emp,'prs6':prs6,'plas6':plas6,'counts__7':counts__7,'counttls7_emp':counttls7_emp,'prs7':prs7,'plas7':plas7,'counts__8':counts__8,'counttls8_emp':counttls8_emp,'prs8':prs8,'plas8':plas8,'counts__9':counts__9,'counttls9_emp':counttls9_emp,'prs9':prs9,'plas9':plas9,'counts__10':counts__10,'counttls10_emp':counttls10_emp,'prs10':prs10,'plas10':plas10,'counts__11':counts__11,'counttls11_emp':counttls11_emp,'prs11':prs11,'plas11':plas11,'counts__12':counts__12,'counttls12_emp':counttls12_emp,'prs12':prs12,'plas12':plas12,'counts__13':counts__13,'counttls13_emp':counttls13_emp,'prs13':prs13,'plas13':plas13})

  


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

                            # 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  akashDjango new tokkens

# sudo mysql -p -u root

# CREATE USER 'USERNAME'@'%' IDENTIFIED BY 'PASSWORD';
# GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'%' WITH GRANT OPTION;

# sudo mysql -u root;
# use mysql;
# UPDATE mysql.user SET plugin = 'mysql_native_password', Password = PASSWORD('pass1234') WHERE User = 'root';
# FLUSH PRIVILEGES;
# exit;


# UPDATE user SET Password='root' WHERE User='root'; FLUSH PRIVILEGES; exit;


   




    



            
  


    


                

        

    
   





               

        

    

    




    





