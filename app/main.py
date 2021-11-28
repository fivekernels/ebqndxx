import os
import sys
import requests
import json
import logging

# https://wp.for-get.com/349.html
# https://blog.csdn.net/rusi__/article/details/100122350
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO
# 第二步，创建一个handler，用于写入日志文件
logfile = '/home/app/info.log'
fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)   # 输出到console的log等级的开关
# 第四步，定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

logging.info('program start')

# global openid, ua
global ua

# # 参数模式
# if len(sys.argv) == 1:
#     logging.info("no argv")
#     sys.exit(1)
# openid = sys.argv[1]

# # 环境变量模式
# openid = os.environ["APP_OPENID"]    #微信openid，系统判别方式
# logging.debug("openid = " + openid)
# # sys.exit(1)

# # 读取openid文件
# openids = []
# for line in open("/home/app/secrets/openids.txt","r"): #设置文件对象并读取每一行文件
#     line = line.replace('\n', '')  # 替换换行符
#     openids.append(line)               #将每一行文件加入到list中
# for i in range(len(openids)):
#     logging.debug("i = " + str(i) + ": " + openids[i])
# sys.exit(1)
# openid = str(openids[0])

# 读取json
f = open("/home/app/secrets/openids.json",'r',encoding='utf-8')
userJsonData = json.load(f)

# for i in range(len(userJsonData)):
#     logging.debug("i = " + str(i) + ", openid = " + userJsonData[i]['openid'])
# sys.exit(1)

# openid = "0"

#模拟微信UA
ua = "Mozilla/5.0 (Linux; Android 10; ELS-NX9 Build/HUAWEIELS-N29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2759 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/1583 MicroMessenger/8.0.1.1840(0x2800013B) Process/tools WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 Edg/95.0.4638.69"
root_url = "http://qndxx.youth54.cn"    #根地址
nvi_url = "/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid="  #获取最新大学习信息
record_url = "/SmartLA/dxxjfgl.w?method=queryPersonStudyRecord&openid=" # 查询所有学习记录
sign_url = "/SmartLA/dxxjfgl.w?method=studyLatest"    #签到地址

# 更新信息后弹出
# http://qndxx.youth54.cn/SmartLA/lottery.w?method=enterMainPage&version=

s = requests.Session()    #建立会话

### 获取最新大学习期数
def getLatestVersion(para_openid):
    r = s.post(root_url + nvi_url + para_openid,data = "", headers = {"User-Agent": ua}, timeout = 30)
    logging.info("response code= " + str(r.status_code))
    version = r.json()['version']
    return version

### 获取当前学习记录
def getStudyRecord(para_openid):
    r = s.get(root_url + record_url + para_openid)
    # logging.debug(r)
    latestRecordData = r.json()['vds'][0]
    return latestRecordData['version']

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
    r = s.post(root_url + sign_url, data = data, headers = headers)
    return r.json()


if __name__ == '__main__':
    # OPENID_1 = os.environ["OPENID_1"]
    # outputstr = "openid = " + OPENID_1
    # logging.debug("openid = " + outputstr[9]+outputstr[10])
    # if outputstr[9] != '1':
    #     sys.exit(1)
    # logging.debug("sucess")

    
    for i in range(len(userJsonData)):
        # logging.debug("i = " + str(i) + ", openid = " + userJsonData[i]['openid'])
        if ( i == 0 ):
            continue
        logging.info("start i = " + str(i))
        openid = userJsonData[i]['openid']

        latestVersion = getLatestVersion(openid)
        logging.info("latestVersion = " + latestVersion)

        latestRecord = getStudyRecord(openid)
        if ( latestVersion == latestRecord ):
            logging.info("already signed")
            continue
            
        logging.info("start to sign")

        response_sign = signNewRecord(latestVersion, openid)
        # logging.debug("response = " + str(response_sign))
        if response_sign['errcode'] != "0":
            logging.info(response_sign['errmsg'])
        else:
            logging.info("sign in sucess, version = " + latestVersion)

    logging.info("exit, bye.")
