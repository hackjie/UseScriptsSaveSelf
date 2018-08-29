# coding=utf-8
# 这是一个查找项目中未国际化的脚本

import os
import re

# 汉语写入文件时需要
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 将要解析的项目名称
DESPATH = "/Users/leoli/Desktop/workspace/git/TuandaiFund/TuandaiFund/Modules/Product/ProductDetail"

# 解析结果存放的路径
WDESPATH = "/Users/leoli/Desktop/unlocalized.log"

#目录黑名单，这个目录下所有的文件将被忽略
BLACKDIRLIST = [
                'Jenkinsfile',
                'podfile',
                'podfile.lock',
                DESPATH + '/Pods',
                DESPATH + '/PrivateEquity',
                'PrivateEquity.xcodeproj',
                'PrivateEquity.xcworkspace'
                ]

# 输出分隔符
SEPREATE = ' <=> '

def isInBlackList(filePath):
    if os.path.isfile(filePath):
        return fileNameAtPath(filePath) in BLACKDIRLIST
    if filePath:
        return filePath in BLACKDIRLIST
    return False

def fileNameAtPath(filePath):
    return os.path.split(filePath)[1]

def isSignalNote(str):
    if '//' in str:
        return True
    if '///' in str:
        return True
    if str.startswith('#pragma'):
        return True
    return False

def isLogMsg(str):
    if str.startswith('NSLog') or str.startswith('FLOG'):
        return True
    return False

def unlocalizedStrs(filePath):
    f = open(filePath)
    fileName = fileNameAtPath(filePath)
    isMutliNote = False
    isHaveWriteFileName = False
    for index, line in enumerate(f):
        #多行注释
        line = line.strip()
        if '/*' in line:
            isMutliNote = True
        if '*/' in line:
            isMutliNote = False
        if isMutliNote:
            continue

        #单行注释
        if isSignalNote(line):
            continue

        #打印信息
        if isLogMsg(line):
            continue

        # OC
        # matchList = re.findall(u'@"[\u4e00-\u9fff]+', line.decode('utf-8'))

        # swift
        matchList = re.findall(u'".*[\u4e00-\u9fff]+', line.decode('utf-8'))
        if matchList:
            if not isHaveWriteFileName:
                wf.write('\n' + fileName + '\n')
                isHaveWriteFileName = True

            for item in matchList:
                wf.write(str(index + 1) + ':' + item[2 : len(item)] + SEPREATE + line + '\n')

def findFromFile(path):
    paths = os.listdir(path)
    for aCompent in paths:
        aPath = os.path.join(path, aCompent)
        if isInBlackList(aPath):
            print('在黑名单中，被自动忽略' + aPath)
            continue
        if os.path.isdir(aPath):
            findFromFile(aPath)
        # OC
        # elif os.path.isfile(aPath) and os.path.splitext(aPath)[1]=='.m':

        # swift
        elif os.path.isfile(aPath) and os.path.splitext(aPath)[1]=='.swift':
            unlocalizedStrs(aPath)

if __name__ == '__main__':
    wf = open(WDESPATH, 'w')
    findFromFile(DESPATH)
    wf.close()

