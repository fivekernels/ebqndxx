# encoding: utf-8

import logging

class CommonLogging(object):
    def __init__(self, logger=None):
        # 1创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO

        if not self.logger.handlers:
            # 2创建一个handler，用于写入日志文件
            self.log_fullname = '/home/app/info.log'
            fh = logging.FileHandler(self.log_fullname, mode='a', encoding='utf-8')  # open的打开模式这里可以进行参考
            fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
            # 3再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)  # 输出到console的log等级
            # 4定义handler的输出格式（时间，文件，函数，行数，错误级别，错误提示）
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s->%(funcName)s [line:%(lineno)d]: %(message)s")
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 5给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            # 关闭打开的文件
            fh.close()
            ch.close()

    def getlog(self):
        return self.logger