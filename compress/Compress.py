# -*- coding: UTF-8 -*-
import os
import random
import time
import shutil

class Compress(object):
    DEBUG = True
    MODE_OVERLAY = 0
    MODE_MOVE = 1
    MODE_EXPLAIN = ["覆盖源文件","在新目录下输出"]
    COUNT_EXEC = 0
    COUNT_IGNORE = 0
    PATCH9 = ".9.png"
    PNG = ".png"
    SUFFIX = [PNG,".jpg","jpeg",".jpe",".jfif",".jif"]

    def checkFile(self, file):
        res = False
        for suf in self.SUFFIX:
            if file.lower().endswith(suf):
                res = True
                break;
        return res


    def ignore(self, file):
        self.log("忽略文件 : " + file)
        self.COUNT_IGNORE += 1

    def execf(self, file):
        self.log("处理文件 : " + file)
        self.COUNT_EXEC += 1

    def log(self, info):
        if self.DEBUG:
            print(info)
            self.logFile.write(info)
            self.logFile.write('\n')

    def listFile(self, root):
            for file in os.listdir(root):
                self.stack.append(root + file)

    def scanFile(self):
        while len(self.stack) != 0 :
            child = self.stack.pop()
            if os.path.isfile(child):
                self.compressImg(child) if self.checkFile(child) else self.ignore(child)
            elif os.path.isdir(child):
                if self.recursive:
                    self.log("进入目录 : " + child)
                    if self.mode == self.MODE_MOVE:
                        os.mkdir(self.imgOut + child.replace(self.imgDir,""))
                    self.listFile(child + "/")

    def compressImg(self, file):
        if file.lower().endswith(self.PATCH9):
            self.ignore(file)
            return
        if file.lower().endswith(self.PNG) :
            self.execf(file)
            if self.mode == self.MODE_OVERLAY:
                os.system("./png --force --ext .png --quality=80 " + file)
            else:
                os.system("./png --force --quality=80 " + file)
                fpath,tfname = os.path.split(file)
                fname,fsuf = os.path.splitext(tfname)
                newJpg = fpath + "/" +fname + "-fs8" + fsuf
                shutil.move(newJpg,self.imgOut + file.replace(self.imgDir,""))
            return
        if self.mode == self.MODE_OVERLAY:
            os.system("./jpg --quality 85" + file + " " + file)
        else:
            os.system("./jpg --quality 85" + file + " " + self.imgOut + file.replace(self.imgDir,""))
        self.execf(file)
        pass

    def run(self):
        self.log("开始执行！ 源文件夹：" + self.imgDir +
                 "  输出模式：" + self.MODE_EXPLAIN[self.mode] +
                 "  遍历模式：" + "递归遍历所有子目录" if self.recursive else "仅遍历一级目录")
        self.listFile(self.imgDir)
        self.scanFile()
        self.log("运行结束！ 所用时间 ：" + str(time.time() - self.startTime) +
                 " 处理文件数量：" + str(self.COUNT_EXEC) +
                 " 忽略文件数量：" + str(self.COUNT_IGNORE) +
                 " 输出目录：" + self.imgOut)
        self.logFile.close()


    def __init__(self, imgDir, mode, recursive, quality):
        self.startTime = time.time()
        self.imgDir = imgDir if imgDir.endswith("/") else imgDir+"/" 
        self.src = os.getcwd() + "/"
        self.mode = mode
        if self.mode == self.MODE_MOVE:
            out = "out" + str(random.uniform(10, 20))[3:]
            try:
                os.mkdir(self.src + out)
                self.imgOut = self.src + out + "/"
            except Exception as e:
                print(e)
                exit(0)
        else:
            self.imgOut = self.imgDir
        self.recursive = recursive
        self.quality = quality
        self.stack = []
        self.match = False
        self.logFile = open(self.imgOut + "log" + str(random.uniform(10, 20))[3:], 'a')