from multiprocessing import Process
import sys
import sqlite3
import os
import logging
import time

class baby(object):
    def __init__(self, name):
        self.name=name
        self.workdir={"DNA":[r"/root/Documents/baby/DNA", r"/root/Documents/baby/DNA/DNA.py"], "baby":[r"/root/Documents/baby/baby"] }
        logging.basicConfig(filename=(self.workdir["baby"][0]+r"/initialize.log"), filemode="w", format="%(asctime)s:%(message)s")
        self.logger=logging.getLogger("init")
        self.logger.setLevel(logging.INFO)
    def initBaby(self):
        self.flag=self.checkBaby()
        if self.flag==1:
            print("creating new baby..Name: {}".format(self.name))
            self.createBaby(self.name)
            self.logger.info("creating new baby, name: {}".format(self.name))
        elif self.flag==2:
            print("awaking {}..".format(self.name))
            self.awakeBaby(self.name)
            self.logger.info("awaking {}..".format(self.name))

    def checkBaby(self):
        if len(self.workdir)==0:
            self.flag=0
            raise Warning("no work directory found, please specify the location of DNA")
        else:
            for item in self.workdir["DNA"]:
                if not os.path.exists(item):
                    self.flag=0
                    raise Warning("DNA file or diectory missing or misconfigured")

            for item in self.workdir["baby"]:
                if not os.path.exists(item):
                    print("no baby created, creat now..")
                    self.flag=1
                    return self.flag

            if os.path.exists(self.workdir["baby"][0]+r"/"+self.name):
                self.flag=2
                return self.flag
            else:
                self.flag=1
                return self.flag

    def createBaby(self, name):
        #create profile directory
        self.bdir=(self.workdir["baby"][0])
        if not os.path.exists(self.bdir):
            os.makedirs(self.bdir)
        self.cwdir=(self.workdir["baby"][0]+r"/"+name)
        if not os.path.exists(self.cwdir):
            os.makedirs(self.cwdir)
            print("creating profile folder for {}".format(name))
            self.logger.info("creating profile folder for {}".format(name))

        #create database
        self.did=(self.cwdir+r"/"+name+".db")
        if not os.path.exists(self.did):
            os.mknod(self.did)
            print("creating database for {}".format(name))
            self.logger.info("creating database for {}".format(name))

        #register profile in database
        conn=sqlite3.connect(self.did)
        c=conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS profile (birthday TEXT, name TEXT, id TEXT, pidBaby NULL)")
        ctime=time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        index=[ctime, self.name, self.cwdir, 'NULL']
        c.execute("INSERT INTO profile VALUES (?,?,?,?)", index)
        conn.commit()
        conn.close()


    def awakeBaby(self, name):
        print("awaking {}".format(name))
        self.logger.info("awaking {}".format(name))

class cell(object):
    def __init__(self, name):
        self.babyName=name
        self.pwdir=r"/root/Documents/baby/baby"+r"/"+self.babyName+r"/cell"
        self.time=time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        (self.fname, suffix)=os.path.splitext(__file__)

    def initCell(self):
        self.checkCell()
        logging.basicConfig(filename=(self.fname+".log"), filemode="w", format="%(asctime)s %(levelname)s: %(message)s")
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO)

        if len(self.checkCell())>=3:
            self.awakeCell("me")
        else:
            self.logger.warning("file missing..") 

    def checkCell(self):
        if not os.path.exists(self.pwdir):
            os.makedirs(self.pwdir)
        self.flist=[]
        for item in os.listdir(os.getcwd()):
            if item.endswith("py"):
                self.flist.append("script exists")
            elif item.endswith("db"):
                self.flist.append("database exists")
            elif item.endswith("config"):
                self.flist.append("config exists")

        return self.flist


    def createCell(self):
        #create work directory
        prefix="cell"
        num=0
        while True:
            suffix="%04d"%num
            ctime=time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            self.name=prefix+ctime+suffix
            self.cwdir=self.pwdir+r"/"+self.name
            try:
                os.makedirs(self.cwdir)
            except:
                num+=1
            else:
                break

        #create database and config files
        os.mknod(self.cwdir+r"/"+"cell.db")
        os.mknod(self.cwdir+r"/"+"cell.config")
        os.mkdir(self.cwdir+r"/package")

        #register info in database
        conn=sqlite3.connect(self.cwdir+r"/"+"cell.db")
        c=conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY AUTOINCREMENT, birthday TEXT, dir TEXT, pidCell NULL, cellStatus TEXT, pidComm NULL, commStatus TEXT, type TEXT, flag TEXT, tag NULL, comment NULL)")
        index=[ctime, self.cwdir, "offline", "offline", "standard", "normal"]
        c.execute("INSERT INTO profile( birthday, dir, cellStatus, commStatus, type, flag) VALUES (?,?,?,?,?,?)", index)
        c.execute("CREATE TABLE IF NOT EXISTS package(id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, dir TEXT, flag TEXT, tag NULL, comment NULL)")
        conn.commit()
        conn.close()

    def awakeCell(self, cellId):
        if cellId=="me":
            print("awaking myself..")
        else:
            print("awaking others..")
