# encoding: utf-8

import os
import sys
import json
import time
import random
import getopt
import requests

from CommonLogging import CommonLogging
from EmailService import SendEmail
from DingBotService import SendDingBotMsg

commlogger = CommonLogging().getlog()

WorkingDir = os.path.split(os.path.realpath(__file__))[0] + '/'

# sys.exit(0)

# global openid, ua
# global ua

# # 参数模式
# if len(sys.argv) == 1:
#     commlogger.info("no argv")
#     sys.exit(1)
# openid = sys.argv[1]

# # 环境变量模式
# openid = os.environ["APP_OPENID"]    #微信openid，系统判别方式
# commlogger.debug("openid = " + openid)
# # sys.exit(1)

# # 读取openid文件
# openids = []
# for line in open("/home/app/secrets/openids.txt","r"): #设置文件对象并读取每一行文件
#     line = line.replace('\n', '')  # 替换换行符
#     openids.append(line)               #将每一行文件加入到list中
# for i in range(len(openids)):
#     commlogger.debug("i = " + str(i) + ": " + openids[i])
# sys.exit(1)
# openid = str(openids[0])

#模拟微信UA
ua = "Mozilla/5.0 (Linux; Android 10; ELS-NX9 Build/HUAWEIELS-N29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2759 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/1583 MicroMessenger/8.0.1.1840(0x2800013B) Process/tools WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 Edg/95.0.4638.69"
root_url = "http://qndxx.youth54.cn"    #根地址
nvi_url = "/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid="  #获取最新大学习信息
record_url = "/SmartLA/dxxjfgl.w?method=queryPersonStudyRecord&openid=" # 查询所有学习记录
sign_url = "/SmartLA/dxxjfgl.w?method=studyLatest"    #签到地址

# http://qndxx.youth54.cn/SmartLA/lottery.w?method=enterMainPage&version= # 更新信息后弹出

# 获取调用参数
def GetArgvs():
    """ 规定并获取运行程序时附加的参数

    :param : None
    :return: [ditt]参数名称-参数值: {"<longopts_1>": <value_1(string or int or ...)>, ...}
    :rtype: dict
    """    
    argvDict = {}
    opts, args = getopt.getopt(sys.argv[1:], '-t:-c:', longopts=['timedelay=', 'caller=']) # 指定参数格式 短格式(':'必须带参数) 长格式(必须对应'='带参数)
    argvDict['caller'] = '<no caller argv>'
    argvDict['timedelay'] = 30*60 # 默认30分钟
    for opt_name, opt_value in opts:
        if opt_name in ('-c', '--caller'):
            argvDict['caller'] = opt_value
        if opt_name in ('-t', '--time'):
            argvDict['timedelay'] = int(opt_value)
    return argvDict

# 读取json
def ReadJsonFile(fileReltivePath):
    f = open(WorkingDir + fileReltivePath,'r',encoding='utf-8')
    userJsonData = json.load(f)
    return userJsonData

s = requests.Session()    #建立会话

### 获取最新大学习期数
def getLatestVersion(para_openid):
    r = s.post(root_url + nvi_url + para_openid,data = "", headers = {"User-Agent": ua}, timeout = 30)
    commlogger.info("response code= " + str(r.status_code))
    try:
        version = r.json()['version']
        commlogger.info("got latest version: " + version)
        return version
    except Exception as e:
        commlogger.error("geting version exception: " + str(e) +  ".r = " + r)
        return None

# 获取当前学习记录
def getStudyRecord(para_openid):
    r = s.get(root_url + record_url + para_openid)
    # commlogger.debug(r)
    try:
        latestRecordData = r.json()['vds'][0]
        commlogger.info("got last record: " + latestRecordData['version'])
        return latestRecordData['version']
    except Exception as e:
        commlogger.warning("catch exception: " + str(e))
        return None

## 签到
def signNewRecord(version, para_openid):    #签到最新一期，书写方式例如"7-7"
    headers = {
        "User-Agent" : ua,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    data = {
        "openid": para_openid,
        "version":version
        }
    try:
        r = s.post(root_url + sign_url, data = data, headers = headers)
        commlogger.debug("response = " + str(r))
        return r.json()
    except Exception as e:
        commlogger.warning("requests post with exception: " + str(e))
        return None

# 发送邮件签到结果
def sendEmailResult(singleUserJson, resultCode):
    try:
        commlogger.info("getting email address")
        reseiverAddress = singleUserJson['email']
    except Exception as e:
        commlogger.info("invalid email address")
        return None

    emailContentFilename = None
    if resultCode == 0: # sucess
        # sucess
        commlogger.info("reading sucess content")
        emailContentFilename = 'Mail-Content_en.txt'
    elif resultCode == 1: # already
        # already
        commlogger.info("reading already content")
        emailContentFilename = 'Mail-Content-already_en.txt'
    else:
        # default
        emailContentFilename = None

    if emailContentFilename is None:
        mailContent = 'default content'
    else:
        mailContentFile = open(WorkingDir + emailContentFilename, 'r', encoding='utf-8')
        mailContent = mailContentFile.read()
        mailContentFile.close()

    SendEmail('dxx auto notice', reseiverAddress, mailContent, 'dxx weekly result')

# 使用钉钉机器人发送签到结果
def sendDingBotResult(singleUserJson, resultCode):
    commlogger.info("sending bot msg...")
    if resultCode == 0: # sucess
        # sucess
        SendDingBotMsg("QNDXX signed in successfully: " + singleUserJson['name'])
    elif resultCode == 1: # already
        # already
        SendDingBotMsg("QNDXX already signed: " + singleUserJson['name'])
    return True

if __name__ == '__main__':

    callerArgvs = GetArgvs() # 获取调用参数
    commlogger.info('program main start, called by ' + callerArgvs['caller'])

    userJsonData = ReadJsonFile('secrets/openids.json') # 读取openid

    delaySeconds = random.randint(0, callerArgvs['timedelay']) # 默认30分钟随机
    commlogger.info("delay " + str(delaySeconds))
    time.sleep(delaySeconds)

    # OPENID_1 = os.environ["OPENID_1"]
    # outputstr = "openid = " + OPENID_1
    # commlogger.debug("openid = " + outputstr[9]+outputstr[10])
    # if outputstr[9] != '1':
    #     sys.exit(1)
    # commlogger.debug("sucess")

    for i in range(len(userJsonData)):
        # commlogger.debug("i = " + str(i) + ", openid = " + userJsonData[i]['openid'])
        if ( userJsonData[i]['enable'] == False ):
            continue
        commlogger.info("start i = %d, name = %s", i, userJsonData[i]['name'])
        openid = userJsonData[i]['openid']

        latestVersion = getLatestVersion(openid)
        latestRecord = getStudyRecord(openid)

        if latestRecord is None:
            commlogger.warning("last record is None, sign in anymore")
        elif ( latestVersion == latestRecord ):
            commlogger.info("already signed")
            # sendEmailResult(userJsonData[i], 1)
            sendDingBotResult(userJsonData[i], 1)
            continue
            
        commlogger.info("starting sign in")
        response_sign = signNewRecord(latestVersion, openid)

        if response_sign is None:
            commlogger.warning("signNewRecord() return None")
        elif response_sign['errcode'] != "0":
            commlogger.warning(response_sign['errmsg'])
        else:
            commlogger.info("sign in successfully, version = " + latestVersion)
            # sendEmailResult(userJsonData[i], 0)
            sendDingBotResult(userJsonData[i], 0)
            commlogger.info("waiting 65s before next user...")
            time.sleep(65) # 65秒延时 后续改为随机

    commlogger.info("finished, bye.")
