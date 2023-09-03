from django.shortcuts import render,redirect
from django.http import HttpResponse;
from django.http import JsonResponse;
from django.contrib.auth.models import User
from app.models import Vaccine
from app.models import User_Vaccines,profile_image,contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import os
from django.core.mail import send_mail
# Create your views here.

def home(request):
    if 'submit' in request.POST:
        name=request.POST.get('name')
        email=request.POST.get('email')
        reason=request.POST.get('reason')
        message=request.POST.get('message')
        contacts = contact(name=name,email=email,reason=reason,message=message)
        contacts.save()
        messages.success(request,"Thank you for reaching,we'll get back to you shortly!")
        return redirect('/home/')
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        uname=request.POST.get('uname')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        conpass = request.POST.get('confirm_password')
        if User.objects.filter(email=email).exists():
            messages.warning(request,'email already registered!!')
            redirect('/login/')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request,'User name already exists!!')
            redirect('/login/')
        elif password!=conpass:
            messages.warning(request,'Passwords doesnot match!!')
        else:
            print(uname,fname,lname,email,password)
            user = User(email=email,password=password,first_name=fname,last_name=lname,username=uname)
            user.set_password(password)
            user.save()
            subject = 'Registration' 
            message = f'Hello! {uname}, Your account has been created successfully' 
            email_from = 'nehapote2003@gmail.com' 
            rec_list = [email] 
            send_mail(subject,message,email_from,rec_list)
            messages.success(request,'User has been registered successfully')
            return redirect('/login/')
    return render(request,'register1.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('uname1')
        password = request.POST.get('password1')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/home/')
        else:
            messages.warning(request,'invalid username or password')
            return redirect('/login/')
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('/home/')

def add_details(request):
    if request.method == 'POST':
        vname = request.POST.get('vname')
        age = request.POST.get('age')
        description = request.POST.get('desc')
        sideEffects = request.POST.get('sideeffects')
        ingredients = request.POST.get('ingredients') 
        image = request.FILES['image']
        vaccine =  Vaccine(vname=vname,age=age,description=description,sideEffects=sideEffects,ingredients=ingredients,image=image,user=request.user)
        vaccine.save()
        messages.success(request,'details added successfully!')
        return redirect('/home/')
    return render(request,'details.html')

def vaccine_list(request,vname):
    if request.method == 'POST':
        vaccines = Vaccine.objects.get(vname=vname)
        queryset = Vaccine.objects.select_related('vid').all()
        vaccinelist = []

        for vaccine in queryset:
            vaccinelist.append({'vname':vaccine.vname,'age':vaccine.age})
        print(vaccinelist)
        return vaccinelist


def vaccine_details(request,id):
    vaccines = Vaccine.objects.get(vid=id)
    uid = request.user
    uid1=request.user.id
    if request.user.is_authenticated:
        user_vaccine = User_Vaccines(vid_id=id,uid=uid)
        count = User_Vaccines.objects.filter(uid_id=uid).filter(vid_id=id).exists()
        if 'Queue' in request.POST:
                if User_Vaccines.objects.filter(uid_id=uid).filter(vid_id=id).exists():
                    messages.warning(request,'vaccine already exists')
                    vaccinelist = User_Vaccines.objects.filter(uid_id=uid)
                    print(vaccinelist)
                    return redirect('/home/')
                else:
                    user_vaccine.save()
                    subject = 'Adding Vaccine' 
                    message = f'Hello! {uid}, Vaccine has been queued successfully' 
                    email_from = 'kulalisushmita21@gmail.com' 
                    email = request.user.email
                    email = email.replace('\n','')
                    email = email.replace('\r','')
                    rec_list = [email] 
                    send_mail(subject,message,email_from,rec_list)
                    messages.success(request,'vaccine added')
                    vaccinelist = User_Vaccines.objects.filter(uid_id=uid)
                    print(vaccinelist)
                    url= '/user_vaccines/'+str(uid1)
                    return redirect(url)
        if 'book' in request.POST:
            return redirect('/home/')
        return render(request,'vaccine_details.html',{'vaccine':vaccines,'user_vaccines':user_vaccine,'count1':count})
    else:
        messages.warning(request,'login to continue')
        return render(request,'vaccine_details.html',{'vaccine':vaccines})


def profile(request,id):
    uid=request.user.id
    user = User.objects.get(id=id)
    # user1 = profile_image.objects.get(user_id=id)
    vaccines = User_Vaccines.objects.filter(uid_id=uid)
    if profile_image.objects.filter(user_id=id).exists():
            pro=profile_image.objects.get(user_id=id)
            image=pro.image
    else:
        image=False
    if 'image' in request.FILES:
        image = request.FILES['image']
    elif image is None:
        image= profile_image.objects.get(image=image)
        print(image)
    user1 = profile_image(user_id= uid,image = image)
    if 'editpro' in request.POST:
        user1.save() 
        return redirect(profile,id)
    return render(request,'profile.html',{'vaccine':vaccines,'users':user,'user1':user1})


def user_vaccines(request,id):
    uid=id
    user = User.objects.get(id=id)
    vaccines = User_Vaccines.objects.filter(uid_id=uid)
    vaccines_count = User_Vaccines.objects.filter(uid_id=uid).count()
    print(vaccines_count)
    return render(request,'user_vaccines.html',{'vaccine':vaccines,'users':user,'vaccines_count':vaccines_count})



def delete_User(request,id):
        uid = request.user
        uid1=request.user.id
        user_vaccine = User_Vaccines.objects.get(vid_id=id,uid_id=uid)
        user_vaccine.delete()
        user = User.objects.get(id=request.user.id)
        vaccines = User_Vaccines.objects.filter(uid_id=uid)
        print(user_vaccine)
        return redirect(user_vaccines,uid1)


def delete_Vaccine(request,id):
    vaccine = Vaccine.objects.get(vid=id)
    print(vaccine)
    vaccine.delete()
    return redirect('/home/')


def Edit_Vaccine(request,id):
    vaccines = Vaccine.objects.get(vid=id)
    if request.method == 'POST':
        vname = request.POST.get('vname')
        age = request.POST.get('age')
        description = request.POST.get('desc')
        sideEffects = request.POST.get('sideeffects')
        ingredients = request.POST.get('ingredients') 
        vaccines.vname = vname
        vaccines.description = description
        vaccines.age = age
        vaccines.sideEffects = sideEffects
        vaccines.ingredients = ingredients
        if len(request.FILES)!=0:
            if len(request.FILES) > 0:
                os.remove(vaccines.image.path)
            vaccines.image = request.FILES['image']
        vaccines.save()
        messages.success(request,'details edited successfully!')
        return redirect('/home/')
    return render(request,'edit.html',{'vaccine':vaccines})


def hm(request):
    return render(request,"hm.html")

def vaccines(request):
    vaccines = Vaccine.objects.all()
    return render(request,'vaccines.html',{'vaccine':vaccines})

def edit_profile(request,id):
        user=User.objects.get(id=id)
        if request.method == 'POST':
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            # new_password=request.POST.get('password')
            # print(new_password)
            user.email = email
            user.first_name = fname
            user.last_name = lname
            # name.set_password(new_password)
            # name.save()
            user.save()
        uid=request.user.id
        if profile_image.objects.filter(user_id=id).exists():
            pro=profile_image.objects.get(user_id=id)
            image=pro.image
        else:
            image=False
        if 'image' in request.FILES:
            image = request.FILES['image']
        elif image is None:
            image= profile_image.objects.get(image=image)
            print(image)
        user1 = profile_image(user_id= id,image = image)
        if 'editpro' in request.POST:
            user1.save() 
            return redirect(profile,id)
        return render(request,'edit_profile.html',{'user1':user1,'users':user})

def change_password(request):
    if request.method == 'POST':
        name=User.objects.get(username=request.user.username)
        new_password=request.POST.get('password')
        print(new_password)
        name.set_password(new_password)
        name.save()
        messages.success(request,"Password changed")
        return redirect("/home/")
    return render(request,"change_password.html")


