import os

if __name__ == '__main__':
    OPENID_1 = os.environ["OPENID_1"]
    outputstr = "openid = " + OPENID_1
    print(outputstr[9]+outputstr[10])