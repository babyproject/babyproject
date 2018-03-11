import sqlite3
import os
import sys
import time
import inspect
import pickle
import shutil
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mtp

class core(object):
    def __init__(self):
        self.cwdir=os.getcwd()
        os.chdir(self.cwdir)
        self.pwdir=os.path.dirname(self.cwdir)
        self.conn=sqlite3.connect("cell.db")
        self.pkgTemp="temp.pkl"
        self.cellScript="cell.py"
        self.commScript="cellComm.py"
        self.c=self.conn.cursor()
        self.package={"mode":"deliver", "from":self.cwdir, "to":[], "time": "null" ,"type": "null" , "tag":[], "dataSet": "null"}

    def execScript(self, scriptName):
        with open(scriptName, "r") as fs:
            exec(fs.read())

    def awakeComm(self, target):
        if target=="self":
            self.c.execute("SELECT commStatus FROM profile")
            if self.c.fetchone()[0]=="offline":
                print("cell: awake cellComm of myself")
                ps=mtp.Process(target=self.execScript, args=(self.commScript,))
                ps.daemon=False
                ps.start()
            else:
                print("cell: the cellComm is online")

        else:
            if os.path.exists(target):
                sys.argv[0]=target
                print("cell: awake cellComm of other cell")
                po=mtp.Process(target=self.execScript, args=(target,))
                po.daemon=False
                po.start()


    #send() function accepts dictionary object 
    def send(self, packageObject):
        self.packageObject=packageObject
        if type(self.packageObject)==dict:
            temp=open(self.pkgTemp, "wb")
            pickle.dump(self.packageObject, temp)
            temp.close()
            for item in self.packageObject["to"]:
                num=0
                commTarget=item+r"/"+self.commScript
                while True:
                    if not os.path.exists(item):
                        print("cell: contact doesn't exists")
                        break

                    suffix="%04d"%num
                    ctime=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
                    pkgDes=item+r"/"+ctime+suffix+".pkl"
                    try:
                        shutil.copy(self.pkgTemp, pkgDes)
                        print("cell: package sended..")
                    except:
                        num+=1
                    else:
                        self.awakeComm(commTarget)
                        break
            os.remove(self.pkgTemp)

    def processing(self):
        self.c.execute("UPDATE profile SET cellStatus='online'")
        self.conn.commit()
        print("cell: set cell online")

        self.pid=os.getpid()
        self.c.execute("UPDATE profile SET pidCell={}".format(self.pid))
        self.conn.commit()

        img=plt.imread("image2.jpg")

        self.package["mode"]="deliver"
        self.package["to"]=[(self.pwdir+r"/cell201801212112090000"), (self.pwdir+r"/cell201801212112070000")]
        ctime=time.strftime("%H%m%d%H%M%S", time.localtime(time.time()))
        self.package["time"]=ctime
        self.package["type"]="image"
        self.package["tag"]="raw"
        self.package["dataSet"]=img[500]

        self.send(self.package)

        plt.figure("image")
        plt.imshow(img)
        plt.show()
        

        self.c.execute("UPDATE profile SET cellStatus='offline'")
        self.c.execute("UPDATE profile SET pidCell='NULL'")
        self.conn.commit()
        print("cell: cell offline")

    def run(self):
        self.processing()

#---------------
ins=core()
ins.run()
#ins.run()
