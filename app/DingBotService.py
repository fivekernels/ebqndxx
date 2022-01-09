import requests
import json

from CommonLogging import CommonLogging

commlogger = CommonLogging().getlog()

WebhookUrlPrefix = "https://oapi.dingtalk.com/robot/send?access_token="

def SendDingBotMsg(message):
    # 读取json
    f = open("/home/app/secrets/ding-bot.json",'r',encoding='utf-8')
    webHookConfig = json.load(f)
    f.close()
    accessToken = webHookConfig['access_token']

    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    r = requests.post(WebhookUrlPrefix+accessToken, json=data)
    if r.status_code == requests.codes.ok:
        if r.json()["errcode"] == 0:
            commlogger.info("response message = " + r.json()["errmsg"])
            return True
        else :
            commlogger.warning("errcode = " + str(r.json()["errcode"]) + ", errmsg = " + r.json()["errmsg"])
            return False
    else :
        commlogger.warning("respose code not 200")
        return False

# SendDingBotMsg("qndxx helloworld 2.0")