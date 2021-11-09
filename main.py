import os
import sys
import requests

# 更新信息后弹出
# http://qndxx.youth54.cn/SmartLA/lottery.w?method=enterMainPage&version=

if __name__ == '__main__':
    OPENID_1 = os.environ["OPENID_1"]
    outputstr = "openid = " + OPENID_1
    print("openid = " + outputstr[9]+outputstr[10])
    if outputstr[9] != 1:
        sys.exit(1)
    print("sucess")