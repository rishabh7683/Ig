from django.shortcuts import render
from .models import Admin, Task,Chunk
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden,HttpResponseRedirect)
from django.contrib.auth.decorators import login_required,user_passes_test
import pandas as pd
import datetime
import numpy as np
import os
import threading
from datetime import datetime
from instagrapi import Client

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/')

        admin_obj = Admin.objects.filter(user = user_obj).first()
        if not admin_obj.is_verified:
            messages.success(request, 'Your account is not verified yet, please contact at keshav@whizco.in')
            return redirect('/')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Invalid Password!')
            return redirect('/')
        login(request , user)
        messages.success(request, 'Logged In Successfully!')
        return redirect('/instagram')
    return render(request , 'login.html')


def register_user(request):
    if request.method == 'POST':
        FullName = request.POST.get('f_name')
        Mobile_Number = request.POST.get('mbl')
        username = request.POST.get('usernameji')
        password = request.POST.get('password')
        ig_password=password
        if User.objects.filter(username = username).first():
            messages.success(request, 'Username is taken.')
            return redirect('/register_user')
        user_obj = User.objects.create(username = username)
        user_obj.set_password(password)
        user_obj.save()
        Admin_obj = Admin.objects.create(user = user_obj , FullName=FullName, Mobile_Number=Mobile_Number,ig_password=ig_password)
        Admin_obj.save()
        return redirect('/verify')
    return render(request, 'registration.html')

def verify(request):
    return render(request, 'verify.html')

@login_required(login_url='login_user')
def instagram(request):
    try:

        taskji=Task.objects.all().filter(owner__user=request.user).first()
        notable=taskji.status
    except:
        notable=True
        pass

    names=Admin.objects.get(user=request.user).FullName
    if 'send' in request.POST:
        username_lst=request.FILES.get('username')
        message=request.POST.get('message')
        cname=request.POST.get('name')
        task_owner = Admin.objects.get(user=request.user)
        try:
            userlst=pd.read_csv(username_lst)
        except:
            userlst=pd.read_excel(username_lst)

        all_username = userlst.iloc[:, 0]
        all_username=list(all_username)
        join=''
        for p in all_username:
            join=join+','+p
        Task_obj = Task.objects.create(
        owner=task_owner,
        task_name=cname,
        all_username=join,
        message=message,
        action_time= datetime.now(),
        )
        Task_obj.save()
        if len(all_username)%7==0:
            count=len(all_username)//7
        else:
            count=len(all_username)//7
            count=count+1
        no=0
        to=0
        for num in range(count):
            small=''
            seven=all_username[no:no+7]
            no=no+7
            if num ==0:
                timeji=datetime.now() + pd.DateOffset(minutes=2)
            else:
                timeji=datetime.now() + pd.DateOffset(minutes=120+to)
                to=to+120
            for p in seven:
                small=small+','+p

            Chunk_obj=Chunk.objects.create(
            owner=task_owner,
            task=Task_obj,
            userji=small,
            message=message,
            execute=timeji,
            )

        messages.success(request, 'Task Created Successfully!!!')

    return render(request,'instagram.html',{'name':names,'notable':notable})


transfer=[]
total=0
new_cl=''

@login_required(login_url='login_user')
def ig_reply(request):
    if 'pending' in request.POST:
        number=request.POST.get('num')
        uname=Admin.objects.get(user=request.user).user.username
        pswrd=Admin.objects.get(user=request.user).ig_password
        newpath = r'C:\IG'
        try:

            # if not os.path.exists(newpath):
            #     os.makedirs(newpath)
            #     cl = Client()
            #     cl.login(uname,pswrd)
            #     cl.dump_settings('C:/IG/dump.json')
            # else:
            cl = Client()
                # cl.load_settings('C:/IG/dump.json')
            cl.login(uname,pswrd)
            global new_cl
            new_cl=cl
            # self.new_cl=cl
        except Exception as e:
            print(e)
            messages.success(request, 'Error in Login')
            return redirect('/instagram')
        a1=cl.direct_threads(0,'unread')
        name=[]
        msg=[]
        usernameji=[]
        for p in a1:
            m=p.dict()
            for s in range(int(number)):
                try:
                    usernameji.append(m['users'][0]['username'])
                except:
                    usernameji.append(None)
                try:

                    name.append(m['thread_title'])
                except:
                    name.append(None)
                try:

                    msg.append(m['messages'][s]['text'])
                except:
                    msg.append(None)
        rep=len(msg)
        reply=['']*rep
        datu=zip(name,usernameji,msg,reply)
        data=pd.DataFrame({'Name':name,'Username':usernameji,'Message':msg})
        print(data)
        print("Calling this")
        global transfer
        transfer=usernameji
        global total
        total = len(name)

        return render(request, 'pending.html',{'datu':datu})
    if 'reply' in request.POST:
        print(transfer)

        print("The name length is ")
        print(total)
        print("I am getting executed")
        result=[]

        for m in range(total):
            result.append(request.POST.get(str(m)))
        print(result)
        print(transfer)
        df=pd.DataFrame({'User Name':transfer,'Message':result})
        new_df=df.dropna()
        new_df = new_df.reset_index(drop = True)
        try:
            for m in range(len(new_df)):
                l=[]
                user_id = new_cl.user_id_from_username(new_df['User Name'][m])
                l.append(user_id)
                new_cl.direct_send(new_df['Message'][m],l)
            messages.success(request, 'Reply Sent Successfully')
        except:
            messages.success(request, 'Error in sending reply')
        return redirect('/instagram')
    return render(request, 'pending.html')



@login_required(login_url='login_user')
def task(request):
    taskji=Task.objects.all().filter(owner__user=request.user).order_by('-id')
    print(taskji)
    for i,tk in enumerate(taskji):
        chunkji=Chunk.objects.all().filter(owner__user=request.user, task=tk).last()
        if chunkji.status == True:
            Task.objects.all().filter(id=tk.id).update(status=True)
        else:
            Task.objects.all().filter(id=tk.id).update(status=False)
    name=Admin.objects.get(user=request.user).FullName
    return render(request,'task.html',{'name':name,'taskji':taskji})

@login_required(login_url='login_user')
def chunk(request,pk):
    taskji=Task.objects.get(id=pk)
    chunkji=Chunk.objects.all().filter(owner__user=request.user, task=taskji).order_by('id')
    name=Admin.objects.get(user=request.user).FullName
    return render(request,'chunk.html',{'name':name,'chunkji':chunkji})

@login_required(login_url='login_user')
def task_delete(request,pk):
    task=Task.objects.get(id=pk)
    chunkji=Chunk.objects.all().filter(owner__user=request.user, task=task)
    print("Chunkji started")
    print(len(chunkji))
    print(chunkji)
    task.delete()
    chunkji.delete()
    return redirect('/task')

@login_required(login_url='login_user')
def chunk_delete(request,pk):
    chunk=Chunk.objects.get(id=pk)
    chunk.delete()
    return redirect('/task')
