from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import datetime, time, timedelta, date
from django.core.exceptions import ObjectDoesNotExist
slots = []
# Create your views here.
def index(request):
    return render(request,'index.html')
def users_login(request):
    if request.POST:
        uname=request.POST['uname']
        pwd=request.POST['password']
        user=authenticate(username=uname,password=pwd)
        if user is not None:
            if user.user_type=='admin':
                messages.success(request,'Welcome to admin dashboard')
                return redirect('/admin-dashboard')
            elif user.user_type=='user':
                ulogid=user.id
                user=UserReg.objects.get(user_login=ulogid)
                request.session['uid']=user.id
                # print(request.session['uid'],'user')
                messages.success(request,'Welcome to user dashboard')
                return redirect('/user-dashboard')
            elif user.user_type=='doctor':
                dlogid=user.id
                doctor=DoctorReg.objects.get(doc_login=dlogid)
                request.session['did']=doctor.id
                # print(request.session['uid'],'user')
                messages.success(request,'Welcome to doctor dashboard')
                return redirect('/doctor-dashboard')
        else:
            messages.success(request,'Login Credentials Invalid, Login again')
            return redirect('/users-login')
    return render(request,'users_login.html')
#admin
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')
def admin_adddepartment(request):
    if request.POST:
        dept=request.POST['dname']
        dadd=Department.objects.create(departmentname=dept)
        dadd.save()
        messages.success(request,'Department added sucessfully')
        return redirect('/admin-adddepartment')
    return render(request,'admin/admin_adddepartment.html')
def admin_viewdepartments(request):
    depts=Department.objects.all().order_by('departmentname')
    return render(request,'admin/admin_viewdepartments.html',{"depts":depts})
def admin_updatedepartment(request):
    deptid=request.GET.get('deptid')
    # print(deptid,'//////////////')
    dept=Department.objects.get(id=deptid)
    if request.POST:
        dupdate=request.POST['dname']
        deptupdated=Department.objects.filter(id=deptid).update(departmentname=dupdate)
        messages.success(request,'Department updated sucessfully')
        return redirect('/admin-viewdepartments')
    return render(request,'admin/admin_updatedepartment.html',{'dept':dept})
def admin_deletedepartment(request):
    deptid=request.GET.get('deptid')
    # print(deptid,'//////////////')
    deptdeleted=Department.objects.filter(id=deptid).delete()
    messages.success(request,'Department deleted sucessfully')
    return redirect('/admin-viewdepartments')
def admin_adddoctor(request):
    departments=Department.objects.all().order_by('departmentname')
    if request.POST:
        imge=request.FILES['dimage']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        dept=request.POST['dept']
        availableday=request.POST['availableday']
        timefrom=request.POST['timefrom']
        timeto=request.POST['timeto']
        uname=request.POST['uname']
        password=request.POST['password']
        logdoctor=Login.objects.create_user(username=uname,password=password,user_type='doctor',view_password=password)
        logdoctor.save()
        docreg=DoctorReg.objects.create(doc_login=logdoctor,availabledays=availableday,timefrom=timefrom,timeto=timeto,doc_image=imge,firstname=fname,lastname=lname,email=email,phone=phone,department_id=dept)
        docreg.save()
        messages.success(request,'Doctor added sucessfully')
        return redirect('/admin-adddoctor')
    return render(request,'admin/admin_adddoctor.html',{'departments':departments})
def admin_viewdoctors(request):
    departments=Department.objects.all().order_by('departmentname')
    deptid=request.GET.get('departmentid')
    # print(deptid,'////////////// from view doctors')
    if deptid:
        doctors=DoctorReg.objects.filter(department_id=deptid)
        # print(doctors,'doctors')
    else:
        doctors=DoctorReg.objects.all()
        # print(doctors,'doctors')
    return render(request,'admin/admin_viewdoctors.html',{"doctors":doctors,"departments":departments})
def admin_filterbydept(request):
    # print('inside filter fn')
    departmentid=request.GET.get('deptid')
    # print(departmentid,'////////////// from filter')
    if departmentid:
        return redirect('/admin-viewdoctors?departmentid='+str(departmentid))
    else:
        return redirect('/admin-viewdoctors')
def admin_viewsingledoctor(request):
    doctorid=request.GET.get('docid')
    doctor=DoctorReg.objects.get(id=doctorid)
    return render(request,'admin/admin_viewsingledoctor.html',{"doctor":doctor})
def admin_updatedoctor(request):
    doctorid=request.GET.get('docid')
    doctor=DoctorReg.objects.get(id=doctorid)
    if request.POST:
        if 'dimage' in request.FILES: 
            imge=request.FILES['dimage']
        else:
            imge=doctor.doc_image
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        if 'dept' in request.POST: 
            dept=request.POST['dept']
        else:
            dept=doctor.department
        if 'availableday' in request.POST: 
            availableday=request.POST['availableday']
        else:
            availableday=doctor.availabledays
        timefrom=request.POST['timefrom']
        timeto=request.POST['timeto']
        docupdate=DoctorReg.objects.filter(id=doctorid).update(availabledays=availableday,timefrom=timefrom,timeto=timeto,doc_image=imge,firstname=fname,lastname=lname,email=email,phone=phone,department_id=dept)
        print(imge,fname,lname,email,phone,dept,availableday,timefrom,timeto,'///////////////////@')
        messages.success(request,'Doctor updated sucessfully')
        return redirect('/admin-viewsingledoctor?docid='+doctorid)
    
    return render(request,'admin/admin_updatedoctor.html',{"doctor":doctor})
def admin_deletedoctor(request):
    doctorid=request.GET.get('docid')
    doctor=DoctorReg.objects.get(id=doctorid)
    doctordelete=Login.objects.filter(id=doctor.doc_login.id).delete()
    messages.success(request,'Doctor deleted sucessfully')
    return redirect('/admin-viewdoctors')

def admin_viewfeedbacks(request):
    appointments=Appointment.objects.filter(appointment_status='Completed',feedback_status='Feedback')
    feedbacks=Feedback.objects.filter(appointment__in=appointments)
    print(feedbacks)
    return render(request,'admin/admin_viewfeedbacks.html',{"appointments":appointments,"feedbacks":feedbacks})
#user
def users_signup(request):
    if request.POST:
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        age=request.POST['age']
        address=request.POST['address']
        place=request.POST['place']
        uname=request.POST['uname']
        password=request.POST['password']
        loguser=Login.objects.create_user(username=uname,password=password,user_type='user',view_password=password)
        loguser.save()
        userreg=UserReg.objects.create(user_login=loguser,firstname=fname,lastname=lname,email=email,phone=phone,age=age,place=place,address=address)
        userreg.save()
        messages.success(request,'User signup sucess, Try Login to continue')
        return redirect('/users-login')
    return render(request,'users_signup.html')
def user_dashboard(request):
   
    return render(request,'user/user_dashboard.html')
def chat(request):
    import chatgui
    return render(request,'user/user_dashboard.html')
def user_viewdoctors(request):
    departments=Department.objects.all().order_by('departmentname')
    deptid=request.GET.get('departmentid')
    # print(deptid,'////////////// from view doctors')
    if deptid:
        doctors=DoctorReg.objects.filter(department_id=deptid)
        # print(doctors,'doctors')
    else:
        doctors=DoctorReg.objects.all()
        # print(doctors,'doctors')
    return render(request,'user/user_viewdoctors.html',{"doctors":doctors,"departments":departments})
def user_filterbydept(request):
    # print('inside filter fn')
    departmentid=request.GET.get('deptid')
    # print(departmentid,'////////////// from filter')
    if departmentid:
        return redirect('/user-viewdoctors?departmentid='+str(departmentid))
    else:
        return redirect('/user-viewdoctors')
def user_viewsingledoctor(request):
    doctorid=request.GET.get('docid')
    doctor=DoctorReg.objects.get(id=doctorid)
    return render(request,'user/user_viewsingledoctor.html',{"doctor":doctor})
def time_slots_with_end(start_time, end_time, interval=60):
    t = start_time
    while t <= end_time:
        endslot = (datetime.combine(datetime.today(), t) +
             timedelta(minutes=interval)).time()
        if endslot > end_time:
            break
        else:
            yield t.strftime('%H:%M'), endslot.strftime('%H:%M')
            t=endslot
        
def user_makeappointment(request):
    list2 = []
    print(request,"requesttttt")
    import datetime as dat
    toda=dat.date.today()
    from datetime import datetime
    fdat=toda.strftime("%Y-%m-%d")
    
    
    if request.POST:
        dateselected = request.POST['appoinment-date']
        doctorid = request.GET.get('docid')
        doctor = DoctorReg.objects.get(id=doctorid)
        start = doctor.timefrom
        end = doctor.timeto
        starttime = start
        endtime = end
        list1 = list(time_slots_with_end(starttime, endtime))
        print(list1)
        slots = list1
        print(slots,"slllll")

        for times in list1:
            print(times[0])
            print(times[1])
            checkslottime=times[0] + ' - '+times[1]
            try:
                checked = Appointment.objects.filter(doctor=doctor, appointment_date=dateselected,slottime=checkslottime, appointment_status='Booked')
                print(checked)
                if checked.exists():
                    print('inside if')
                else:
                    print('inside else')
                    list2.append(times)
            except ObjectDoesNotExist:
                pass
        return render(request, 'user/user_makeappointment.html', {'time_slots': list2, 'dateselected': dateselected, 'doctorid': doctorid,'toda':fdat})
    return render(request, 'user/user_makeappointment.html',{'toda':fdat})
def user_add_appointment(request):
    if request.POST:
        doctorid=request.POST['doctorid']
        doctor=DoctorReg.objects.get(id=doctorid)
        print(doctor)
        userid=request.session['uid']
        user=UserReg.objects.get(id=userid)
        print(user)
        selectedslot=request.POST['selectedslot']
        print(selectedslot,'################')
        dateselected=request.POST['appoinment-date']
        print(dateselected,'################')
        appointmentadd=Appointment.objects.create(user=user,doctor=doctor,appointment_date=dateselected,slottime=selectedslot)
        appointmentadd.save()
        messages.success(request,'Your appointment added sucessfully')
        return redirect('/user-viewappointments')
    return redirect('/user-dashboard')
def user_viewappointments(request):
    userid=request.session['uid']
    user=UserReg.objects.get(id=userid)
    print(user)
    appointments=Appointment.objects.filter(user=user,appointment_status='Booked')
    return render(request,'user/user_viewappointments.html',{"appointments":appointments})
def user_changeappointment(request):
    doctorid=request.GET.get('docid')
    appointmentid=request.GET.get('appointmentid')
    appointment=Appointment.objects.filter(id=appointmentid).delete()
    return redirect('/user-makeappointment?docid='+doctorid)
def user_deleteappointment(request):
    appointmentid=request.GET.get('appointmentid')
    appointment=Appointment.objects.filter(id=appointmentid).delete()
    messages.success(request,'Appointment deleted sucessfully')
    return redirect('/user-viewappointments')
def user_viewhistory(request):
    userid=request.session['uid']
    user=UserReg.objects.get(id=userid)
    print(user)
    appointments=Appointment.objects.filter(user=user,appointment_status='Completed')
    feedbacks=Feedback.objects.filter(appointment__in=appointments)
    print(feedbacks)
    return render(request,'user/user_viewhistory.html',{"appointments":appointments,"feedbacks":feedbacks})
def user_addfeedback(request):
    appointmentid=request.GET.get('appointmentid')
    print(appointmentid,'///////////////////')
    if request.POST:
        feed=request.POST['feedbacktext']
        feedadd=Feedback.objects.create(appointment_id=appointmentid,feedback_text=feed)
        feedadd.save()
        appointmentupdate=Appointment.objects.filter(id=appointmentid).update(feedback_status='Feedback')
        messages.success(request,'Feedback added sucessfully')
        return redirect('/user-viewhistory')
    return render(request,'user/user_addfeedback.html')
def user_viewprofile(request):
    userid=request.session['uid']
    user=UserReg.objects.get(id=userid)
    print(user.firstname,'//////////////')
    return render(request,'user/user_viewprofile.html',{'user':user})
def user_updateprofile(request):
    userid=request.GET.get('userid')
    user=UserReg.objects.get(id=userid)
    print(user.firstname,'//////////////')
    if request.POST:
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        age=request.POST['age']
        address=request.POST['address']
        place=request.POST['place']
        userupdate=UserReg.objects.filter(id=userid).update(firstname=fname,lastname=lname,email=email,phone=phone,age=age,place=place,address=address)
        messages.success(request,'User updated sucessfully,,,')
        return redirect('/user-viewprofile')
    return render(request,'user/user_updateprofile.html',{'user':user})
def user_deleteprofile(request):
    userid=request.GET.get('userid')
    user=UserReg.objects.get(id=userid)
    print(user.user_login.id,'//////////////')
    userlogindelete=Login.objects.filter(id=user.user_login.id).delete()
    messages.success(request,'User deleted sucessfully,,,')
    return redirect('/')
#doctor
def doctor_dashboard(request):
    return render(request,'doctor/doctor_dashboard.html')
def doctor_viewappointments(request):
    doctorid=request.session['did']
    print(doctorid,'///////////////////')
    doctor=DoctorReg.objects.get(id=doctorid)
    print(doctor)
    if  request.POST:
        
        ddate_str=request.POST['doctor-date']
        ddate = datetime.strptime(ddate_str, '%Y-%m-%d').date()  # Convert the string to a date object 
        if ddate==date.today():
            datebool='todaysdate'
        else:
            datebool='differentdate' 
    else:
        ddate=date.today()
        datebool='todaysdate'
        print(ddate,'ddate,,,,,,,,,,,,,,,,,,,,')
    print(datebool,ddate,date.today(),',ddate,datebool')
    appointments=Appointment.objects.filter(doctor=doctor,appointment_date=ddate,appointment_status='Booked')
    return render(request,'doctor/doctor_viewappointments.html',{"appointments":appointments,"ddate":ddate,"datebool":datebool})
def doctor_changeappointmentstatus(request):
    appointmentid=request.GET.get('appointmentid')
    print(appointmentid,'///////////////////')
    appointment=Appointment.objects.filter(id=appointmentid).update(appointment_status='Completed')
    print(appointment)
    messages.success(request,'Appointment status changed sucessfully')
    return redirect('/doctor-viewappointments')
def doctor_viewfeedbacks(request):
    doctorid=request.session['did']
    print(doctorid,'///////////////////')
    doctor=DoctorReg.objects.get(id=doctorid)
    print(doctor)
    appointments=Appointment.objects.filter(doctor=doctor,appointment_status='Completed',feedback_status='Feedback')
    feedbacks=Feedback.objects.filter(appointment__in=appointments)
    print(feedbacks)
    return render(request,'doctor/doctor_viewfeedbacks.html',{"appointments":appointments,"feedbacks":feedbacks})