import sqlite3
import os
import time
import inspect

class core(object):
    def __init__(self):
        self.connCell=sqlite3.connect("cell.db")
        self.pkgTemp="temp.pkl"
        self.cellScript="cell.py"
        self.commScript="cellComm.py"
        self.cCell=self.connCell.cursor()
        self.cwdir=self.getcwdir()
        self.pwdir=os.path.dirname(self.cwdir)
        os.chdir(self.cwdir)
        self.packageSample={"mode":"join", "from":"id123", "to":[(self.pwdir+r"/cell"+"201801200453020000")], "time":"20181012122123","type":"unknown", "tag":["dog", "white"], "dataSet":"image object"}


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
                print("awake cellComm of myself")
                ps=mtp.Process(target=self.execScript, args=(self.commScript,))
                ps.daemon=False
                ps.start()
            else:
                print("the cellComm is online")

        else:
            if os.path.exists(target):
                print("awake cellComm of other cell")
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
                        self.awakeComm(commTarget)
                    except:
                        num+=1
                    else:
                        break
            os.remove(self.pkgTemp)

    def processing(self):
        self.cCell.execute("UPDATE profile SET cellStatus='online'")
        self.connCell.commit()

        self.pid=os.getpid()
        self.cCell.execute("UPDATE profile SET pidCell={}".format(self.pid))
        self.connCell.commit()

        print("cell running...")
        print("message received, processing")
        time.sleep(3)
        

        self.cCell.execute("UPDATE profile SET cellStatus='offline'")
        self.cCell.execute("UPDATE profile SET pidCell='NULL'")
        self.connCell.commit()
        print("cell offline")

    def run(self):
        self.processing()

#---------------
ins=core()
ins.run()
