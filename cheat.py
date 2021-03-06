#!/usr/bin/env python
# -*- coding: utf-8 -*-
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from pprint import pprint
import urllib2
import os
import json
import shutil
import time
import random
IMAGE_ROOT_DIR = "images"
LOG_FILE = "upload.log"
SET_MAX = 9
DONE_IMAGE = "doneImages"

#protocol related
HEADER_BDUSS = "BDUSS=1EZmpJUDljb3BPVlVLREdPMm12bktSY1VwTHN0Y2VUalNwSmlIdExZVXFDVjFXQVFBQUFBJCQAAAAAAAAAAAEAAADABr54AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACp8NVYqfDVWWk"
UID = "432345566253059807"
LOCATION = "北京市开拓北路"
LATITUDE = 40.05761
LONGITUDE = 116.307337

def post(post_data):
    register_openers()

    datagen, headers = multipart_encode(post_data)
    request = urllib2.Request("http://image.baidu.com/app/uploadfile", datagen, headers)
    #request = urllib2.Request("http://127.0.0.1/test.php", datagen, headers)
    request.add_header("Cookie", "BDUSS=1EZmpJUDljb3BPVlVLREdPMm12bktSY1VwTHN0Y2VUalNwSmlIdExZVXFDVjFXQVFBQUFBJCQAAAAAAAAAAAEAAADABr54AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACp8NVYqfDVWWk")
    return urllib2.urlopen(request).read()

def genPostData(imageFile, description, tags, seq, setId = -1):
    return {
        "uid":UID,
        "description": description,
        "location":LOCATION,
        "latitude":LATITUDE,
        "longitude":LONGITUDE,
        "picSeq":seq,
        "setId":setId,
        "tags[]":tags,
        "appversion":1.3,
        "devType":0,
        "uploadFile": open(imageFile, "rb"),
        "clientInfo":"model%3AMI+3C%3B+manufacturer%3AXiaomi%3B+iMEI%3A865009029306649%3B+osVersion%3A4.4.4%3B+deviceInfo%3AMI+3C_4.4.4_19_Xiaomi%3B+versionName%3A0.8%3B+versionCode%3A400081%3B+",
        "version":400090
    }
def logV(tag, content):
    log = "V %s :%s\n" % (tag, content)
    print log
    _write_to_log(log)
def logE(tag, content):
    log = "E %s :%s\n" % (tag, content)
    print log
    _write_to_log(log)
def _write_to_log(content):
    output = open(LOG_FILE, 'a')
    output .write(content)
    output .close( )

def postSet(imageFileList, description, tags):
    logV("post", "Post %s set" % description)
    try :
        postData = genPostData(imageFileList.pop(), description, tags, 0, -1)
        setInfoJson = post(postData);
        setInfo = json.loads(setInfoJson)
        setId = setInfo['data']['setId']
        logV("post", "Post set %s " % setId)
        for i in range(len(imageFileList)) :
            if i > 8 :
                break
            post(genPostData(imageFileList[i], description, tags, i + 1, setId))
    except Exception as e:
        logE("postSet", e)
        return False

    return True

def init():
    if not os.path.isdir(DONE_IMAGE):
        os.mkdir(DONE_IMAGE)
    if not os.path.isdir(IMAGE_ROOT_DIR):
        print "No image path defined!"
        exit()
if __name__ == '__main__':
    init()

    protectFlag = True
    imageDirList = os.listdir(IMAGE_ROOT_DIR)
    for tempDir in imageDirList:
        dirPath = os.path.join(IMAGE_ROOT_DIR, tempDir)
        if os.path.isdir(dirPath):
            success = False
            imageList = []
            desc = tempDir
            tags = []
            TAG_TABLE = ["美女", "写真", "漂亮", "清纯", "妹子", "美女写真", "美丽"]
            for i in range(4):
                tagPos = random.randint(0, len(TAG_TABLE) - 1)
                tags.append(TAG_TABLE[tagPos])
                del TAG_TABLE[tagPos]

            for image in os.listdir(dirPath):
                imageList.append(os.path.join(dirPath, image))

            if len(imageList) == 0:
                logV("cheat", "move empty folder %s to done" % tempDir)
                shutil.move(dirPath, DONE_IMAGE)
            else:
                success = postSet(imageList, desc, tags)

                if success:
                    logV("cheat", "upload %s succeed" % tempDir)
                    shutil.move(dirPath, DONE_IMAGE)
                else :
                    logE("cheat", "upload %s failed" % tempDir)
                time.sleep(60)

