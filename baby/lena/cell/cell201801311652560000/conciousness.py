import os
import sys
import time
import sqlite3
import shutil

class(object):
    def __init__(self):
        self.cwdir=os.path.dirname(os.path.abspath(argv[0]))
        os.chdir(self.cwdir)
        self.conn=sqlite3.connect("cell.db")
        self.c=self.conn.cursor()
        self.jumpToLoop()

    def jumpToLoop(self):
        while True:
            self.data=self.read("cmd", "dataSet")
            if self.data=="sleep":
                self.sleep()

    def notion(self):
        pass

    def sleep(self):
        pass


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

