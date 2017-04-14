#!/usr/bin/env python
import os
#os.system(' scrapy crawl dmoz')
import threading
from time import ctime,sleep
import time
listlen=2
sl=100


threads=[]
def doe(fun):
    if(fun==0):
        os.system('scrapy crawl 58ershoufang -a listlen=%d'%listlen)
        sleep(sl)
   	
#	 os.system('scrapy crawl anjuke -a listlen=%d'%listlen)
    if(fun==1):
        os.system('scrapy crawl ganjizufang -a listlen=%d'%listlen)
        sleep(sl)
    if(fun==2):
        os.system('scrapy crawl ganjiershoufang -a listlen=%d'%listlen)
        sleep(sl)
    if(fun==3):    
	os.system('scrapy crawl soufang -a listlen=%d'%listlen)
    	sleep(sl)
    if(fun==4):
	os.system('scrapy crawl soufangershou -a listlen=%d'%listlen)
   	sleep(sl)
def init():
    for i in range(5):
        t =threading.Thread(target=doe,args=(i,))
        threads.append(t)
def run():
    #print("starttime")
    #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #print(threads)
    for i in threads:
	    i.start()
    for i in threads:
	    threads.remove(i)
    i.join(1800)
    #print("endtime")
    init()
    run()
init()
#run()
doe(0)