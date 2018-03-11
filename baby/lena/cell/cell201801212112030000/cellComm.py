import os
import sys
import pickle
import types
import shutil
import time
import sqlite3
import inspect
import multiprocessing as mtp

#packageSample={"mode":"join", "from":"abspath", "to":["id234", "abspath"], "time":"20181012122123","type":"unknown", "tag":["dog", "white"], "dataSet":"image object"}

class cellComm(object):
    def __init__(self):
        self.cwdir=os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(self.cwdir)
        self.pwdir=os.path.dirname(self.cwdir)
        self.conn=sqlite3.connect("cell.db")
        self.c=self.conn.cursor()
        self.pklTemp="temp.pkl"
        self.commScript="cellComm.py"
        self.cellScript="cell.py"
    

    def execScript(self, scriptName):
        with open(scriptName) as fs:
            exec(fs.read())

    def recv(self):
        self.c.execute("UPDATE profile SET commStatus='online'")
        self.conn.commit()
        doList=[]
        print("cellComm: set commSatus online")
        while True:
            for item in os.listdir(self.cwdir):
                if item.endswith("pkl"):
                    doList.append(item)
            if not len(doList)==0:
                for pfile in doList:
                    self.pkgSort(pfile)
                    doList.remove(pfile)
            else:
                print("cellComm: all package sorted")
                self.awakeCell("self")
                self.killComm()
                print("cellComm: set commStatus offline")
                break

    def pkgSort(self, pfile):
        num=0
        while True:
            if os.path.exists(pfile):
                suffix="%04d"%num
                ctime=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
                pkgDes=self.cwdir+r"/package/"+ctime+suffix+".pkl"
                try:
                    shutil.copy(pfile, pkgDes)
                except:
                    num+=1
                else:
                    index=[ctime,  pkgDes, "ready"]
                    self.c.execute("INSERT INTO package (time, dir, flag) VALUES (?,?,?)", index)
                    self.conn.commit()
                    os.remove(pfile)
                    break
            else:
                break

    def awakeCell(self, target):
        self.target=target
        if self.target=="self":
            self.c.execute("SELECT cellStatus FROM profile")
            if self.c.fetchone()[0]=="offline":
                print("cellComm: awake cell..")
                ps=mtp.Process(target=self.execScript, args=(self.cellScript,))
                ps.daemon=False
                ps.start()
            else:
                print("cellComm: the cell is online")

        else:
            if os.path.exists(self.target):
                sys.argv[0]=self.target
                print("call other cell")
                po=mtp.Process(target=self.execScript, args=(target,))
                po.daemon=False
                po.start()

    
    def killComm(self):
        self.c.execute("UPDATE profile SET commStatus='offline'")
        self.conn.commit()

    def run(self):
        self.recv()

#--------------
ins=cellComm()
ins.run()
