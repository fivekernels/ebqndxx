import os
import sys
import requests

global openid, ua
openid = os.environ["OPENID_1"]    #微信openid，系统判别方式
userarg1 = sys.argv[1]
print(userarg1)
#模拟微信UA
ua = "Mozilla/5.0 (Linux; Android 10; ELS-NX9 Build/HUAWEIELS-N29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2759 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/1583 MicroMessenger/8.0.1.1840(0x2800013B) Process/tools WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 Edg/95.0.4638.69"
root_url = "http://qndxx.youth54.cn"    #根地址
nvi_url = "/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid=" + openid  #获取最新大学习信息
sign_url = "/SmartLA/dxxjfgl.w?method=studyLatest"    #签到地址

# 更新信息后弹出
# http://qndxx.youth54.cn/SmartLA/lottery.w?method=enterMainPage&version=

s = requests.Session()    #建立会话

###获取最新大学习期数
def getLatestVersion():
    r = s.post(root_url + nvi_url,data = "", headers = {"User-Agent": ua}, timeout = 30)
    print("response code= " + str(r.status_code))
    version = r.json()['version']
    return version

##签到
def sign(version = '9-b'):    #签到最新一期，书写方式例如"7-7"
    headers = {
        "User-Agent" : ua,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    data = {
        "openid": openid,
        "version":version
        }
    r = s.post(root_url + sign_url, data = data, headers = headers)
    # print(r.json())
    return r.json()


if __name__ == '__main__':
    # OPENID_1 = os.environ["OPENID_1"]
    # outputstr = "openid = " + OPENID_1
    # print("openid = " + outputstr[9]+outputstr[10])
    # if outputstr[9] != '1':
    #     sys.exit(1)
    # print("sucess")
    latestVersion = getLatestVersion()
    print("latestVersion = " + latestVersion)

    response_sign = sign(latestVersion)
    print("response = " + str(response_sign))
    if response_sign['errcode'] != "0":
        print(response_sign['errmsg'])
        sys.exit(1)
    else:
        print("sign in sucess, version = " + latestVersion)
