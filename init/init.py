import sys
sys.path.append(r"/root/Documents/baby/DNA")
import DNA
import threading

class init(object):
    def __init__(self, name):
        self.name=name

    def check(self):
        print("status ok!")

    def run(self):
        print("{} is running..".format(self.name))

ins01=init("John")
ins01.check()
ins01.run()

ins02=init("Hans")
ins02.check()
ins02.run()
