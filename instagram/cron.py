from .models import *
import requests
from datetime import datetime
import pandas as pd
from instagrapi import Client
from time import sleep
import time
import os
from instagrapi import Client
from time import sleep
import time
import os
import random


def send_message():
    now_time=datetime.now()
    ten_time=datetime.now()-pd.DateOffset(minutes=10)
    sending=Chunk.objects.all().filter(execute__range=[now_time, ten_time]).order_by('-id')
    print("I am gonna print")
    print(len(sending))
    print(sending)
    for send in sending:
        owner=send.owner
        usr=send.userji
        msg=send.message
        chunk_id=send.id
        cl = Client()
        try:
            cl.login(owner.user.username,owner.ig_password)
        except:
            chk=Chunk.objects.all().filter(id=chunk_id).update(status=True,user_sent=",LOGIN ERROR",user_notsent=",LOGIN ERROR")
            break
        USERNAME=usr.split(',')
        sent=[]
        notsent=[]
        for i,one in enumerate(USERNAME[1:]):
            try:
                l=[]
                r_time=random.randint(15,25)
                sleep(r_time)
                user_id = cl.user_id_from_username(one)
                l.append(user_id)
                if '{}' in msg:
                    msg=msg.replace('{}',one)
                try:
                    cl.direct_send(msg,l)
                    sent.append(one)
                    print("Message send to "+one)
                except:
                    sleep(4)
                    try:
                        cl.direct_send(msg,l)
                        sent.append(one)
                        print("Message send to " +one)
                    except:
                        notsent.append(one)
                        print("Message not send to "+one)
            except Exception as e:
                print("Danger")
                print(e)

        all_sent=''
        all_notsent=''
        for p in sent:
            all_sent=all_sent+','+p
        for p in notsent:
            all_notsent=all_notsent+','+p
        chk=Chunk.objects.all().filter(id=chunk_id).update(status=True,user_sent=all_sent,user_notsent=all_notsent)
