#########################
# 机构、企业名实体抽取，通过布隆过滤器进行匹配
#########################
import sys
import os
import logging
import json
import pickle
import time
from pybloom_live import BloomFilter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PATH = os.path.dirname(os.path.abspath(__file__))
DUMP_FILE = os.path.join(PATH, "companys.pkl")
COMPANY_FILE = os.path.join(PATH, "companys.txt")

if not os.path.exists(DUMP_FILE):
    logger.info("公司名称pkl文件本地不存在, 需要重新加载")

f = open(DUMP_FILE, "rb")
data = pickle.load(f)
f.close()

class OrganizationExtract():
    def __init__(self):
        logger.info("公司名称识别组件加载公司名称")
        start_time = time.time()
        ## bloom filter文件加载
        if not os.path.exists(DUMP_FILE):
            logger.info("公司名称pkl文件本地不存在, 需要重新加载")
            
        else:
            logger.info("公司名称文件本地存在")
            f = open(DUMP_FILE, "rb")
            data = pickle.load(f)
            self.bloom = data["bloom"]
        end_time = time.time()
        logger.info("企业名称加载完成, 耗时 {} 秒".format(str(int(end_time - start_time))))

    def dumps(self):
        if self.bloom and self.dict:
            data = {
                "bloom": self.bloom,
                "dict": self.dict
            }
            f = open(DUMP_FILE, "wb")
            pickle.dump(data, f)
            logger.info("公司名称文件持久化完成")
        else:
            logger.error("Error! 公司名称内容未准备就绪")


    def process(self, news):
        logger.info("进入企业名识别组件")
        entities = []
        for i in range(2, 21):
            for j in range(0, len(news) - i + 1):
                word = news[j : j + i]
                if word in self.bloom:
                    ## 简称转全称
                    if word in self.dict:
                        word = self.dict[word]

                    entity = {}
                    entity["name"] = word
                    entity["reference"] = {
                        "start": j,
                        "end": j + i}
     