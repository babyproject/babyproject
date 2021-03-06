import sqlite3
import os
import sys
import time
import inspect
import pickle
import shutil
import types
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mtp

class core(object):
    def __init__(self):
        self.cwdir=os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(self.cwdir)
        self.pwdir=os.path.dirname(self.cwdir)
        self.conn=sqlite3.connect("cell.db")
        self.pkgTemp="temp.pkl"
        self.cellScript="cell.py"
        self.commScript="cellComm.py"
        self.c=self.conn.cursor()
        self.package={"mode":"deliver", "from":self.cwdir, "to":[], "time": "null" ,"type": "null" , "tag":[], "dataSet": "null"}


    def getcwdir(self):
        script=inspect.getfile(inspect.currentframe())
        cwdir=os.path.abspath(os.path.dirname(script))
        return cwdir

    def execScript(self, scriptName):
        with open(scriptName, "r") as fs:
            exec(fs.read())

    def awakeComm(self, target):
        if target=="self":
            self.c.execute("SELECT commStatus FROM profile")
            if self.c.fetchone()[0]=="offline":
                sys.argv[0]=target
                print("cell: awake cellComm of myself")
                ps=mtp.Process(target=self.execScript, args=(self.commScript,))
                ps.daemon=False
                ps.start()
            else:
                print("cell: the cellComm is online")

        else:
            if os.path.exists(target):
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
                        break

                    suffix="%04d"%num
                    ctime=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
                    pkgDes=item+r"/"+ctime+suffix+".pkl"
                    try:
                        shutil.copy(self.pkgTemp, pkgDes)
                        print("package sended..")
                    except:
                        num+=1
                    else:
                        self.awakeComm(commTarget)
                        break
            os.remove(self.pkgTemp)

    def read(self, pkgFlag, pklFlag):
        self.c.execute("SELECT dir FROM package WHERE flag==? LIMIT 0,1", (pkgFlag,))
        record=self.c.fetchall()
        if record:
            self.pklFile=record[0][0]
            fs=open(self.pklFile, "rb")
            data=pickle.load(fs)
            return data[pklFlag]
        else:
            return False

    def singularPoint(self, inputData, box, step, samply):
        lis=[]
        for x in range(box[0], len(inputData)-box[0], 2*box[0]):
            for px in range(x-box[0], x+box[0], samply):
                if inputData[px] not in range(inputData[x]-box[1], inputData[x]+box[1]):
                    lis.append((px, inputData[px]))
        lis=list(set(lis))
        return lis


    def processing(self):
        self.c.execute("UPDATE profile SET cellStatus='online'")
        self.conn.commit()
        print("cell: set cell online")

        self.pid=os.getpid()
        self.c.execute("UPDATE profile SET pidCell={}".format(self.pid))
        self.conn.commit()
        
        try:
            print("cell: received, processing----------------------------------------")
            data=self.read("ready", "dataSet")
            if type(data)==np.ndarray:
                print("processing data++++++++++++++++++++++++++++++++")
                dim=data.ndim
                channel=len(data[0])
                lis=np.hsplit(data, channel)
                self.result=[]
                for item in range(channel):
                    sp=self.singularPoint(lis[item].flatten(), [10, 10], 20, 4)
                    self.result.append(sp)
                x=[]
                y=[]
                for point in self.result[0]:
                    x.append(point[0])
                    y.append(point[1])
                plt.figure("singularPoint")
                plt.scatter(x, y)
                plt.show()
                self.c.execute("DELETE FROM package WHERE dir=?", (self.pklFile,))
                self.conn.commit()
                os.remove(self.pklFile)
        except:
            print("something goes wrong")

        finally:
            self.c.execute("UPDATE profile SET cellStatus='offline'")
            self.c.execute("UPDATE profile SET pidCell='NULL'")
            self.conn.commit()
            print("cell: finished cell offline")

    def run(self):
        self.processing()

#---------------
ins=core()
ins.run()
