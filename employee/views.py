from django.shortcuts import render,get_object_or_404
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from employee.forms import UserForm
from employee.models import *
    #context is the dictionary which include our key values which we want to send to html
        #Now check username is correct according to DB so we use authenticate method
                    #user_success is the name which we passed into the url



def user_login(request):
    context={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            
            return HttpResponseRedirect(reverse('user_success'))
        else:
            context['error']="provide valid credentials!!!"
            return render(request,'auth/login.html',context)
    else:
        return render(request,'auth/login.html',context)
     

def user_logout(request):
    if request.method=="POST":
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

def success(request):
    context={}
    context['user']=request.user
    return render(request,'auth/success.html',context)

def employee_list(request):

    context={}
    context['users']=User.objects.all()
    context['title']=' Employees'

    return render(request,'employee/index.html',context)


def employee_details(request,id=None):

    context={}
    context['user']=get_object_or_404(User,id=id)
    profile=Profile.objects.get(user_id=id)
    
    context['profile']=profile
    return render(request,'employee/details.html',context)

def employee_add(request):
    context={}
    if request.method == "POST":
        user_form = UserForm(request.POST)
        context['user_form']=user_form
        if user_form.is_valid():
           u=user_form.save()
           return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/add.html',context)

    else:
        user_form=UserForm()
        context['user_form']=user_form
        return render(request,'employee/add.html',context)

def employee_edit(request,id=None):

    user= get_object_or_404(User, id=id)
    if request.method=="POST":
        user_form = UserForm(request.POST,instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("employee_list"))
        else:
            return render(request,'employee/edit.html',{"user_form":user_form})
    else:
        user_form=UserForm(instance=user)
        return render(request,'employee/edit.html',{"user_form":user_form})

def employee_delete(request,id=None):

    user=get_object_or_404(User,id=id)
    if request.method=="POST":
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context={}
        context['user']=user
        return render(request,'employee/delete.html',context)