#coding=utf8
"""
url：https://xin.baidu.com/
百度企业信用

接口url:http://127.0.0.1:8080/
"""
from flask import abort, jsonify, Flask, request, Response
from bs4 import BeautifulSoup
import logging
import pymongo
import base64
import time, requests
import datetime, random
from etl.utils.log_conf import configure_logging
import traceback
from etl.data_gather.settings import SAVE_MONGO_CONFIG, RESOURCE_DIR
from etl.common_spider.donwloader import Downloader
import json
import re
import pymongo


app = Flask(__name__)
@app.route("/")
def index():
	return "hello world"

# request
@app.route('/company_full_name/<string:sim_name_each>', methods=['GET'])


def run(sim_name_each):
    '''
    数据采集入口
    :return:
    '''
    # logger.info("Begin Run")
    # ============主页面获取==============================
    record = {}
    company_full_name_list = []
    cur_url = "%s%s&t=0" % (api_url, sim_name_each)
    print(cur_url)
    print(sim_name_each)

    for rr in range(10):
        resp = downloader.crawl_data(cur_url, None, headers, "get", )  # 使用downloader文件的ip代理请求
        if resp:

            resp.encoding = 'utf-8'
            content = resp.text
            # print(content)
            # try:
            pat = "window.pageData = (?P<a>(\{.*\}));"
            g = re.search(pat, str(content))

            try:
                text = g.group("a")
                # print(text)
                p = re.search("class=\"[^>]*\"", text)
                # print(p.group())
                t = re.sub("class=\"[^>]*\"", "", text)
                data = json.loads(t)
                print(len(data["result"]["resultList"]))
                r = data["result"]["resultList"]
                if r:
                    for each_n in r:

                        name = each_n['titleName']
                        if name:
                            company_full_name_list.append(name)
                else:
                    print('没有company_full_name')
                    company_full_name_list.append(sim_name_each)

                record["company_full_name"] = company_full_name_list
                return record["company_full_name"]

                # except Exception as e:
                #     print(e)
                #     result = sim_name_each
                #     return result
            except:
                print(content)

        else:
            time.sleep(1)
    return []

if __name__ == '__main__':
    host = "aiqicha.baidu.com"  # 网站域名
    host_name = "百度企业信用"  # 网站中文名
    api_url = "https://aiqicha.baidu.com/s?q="
    start_down_time = datetime.datetime.now()
    down_retry = 5
    configure_logging("11_24.log")
    logger = logging.getLogger("spider")
    downloader = Downloader(logger, need_proxy=False)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        'Host': host,
    }

    # app.run(debug=True, port=8080)

    flag = 0

    # client = pymongo.MongoClient('..', ..)
    # db1 = client...
    # col1 = db1...


    with open('企业简称名单.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            c_clean = i.strip()
            try:
                search_key = c_clean
                a = run(c_clean)
                if a:
                    print(a[0])
                    with open('企业简称名单_revise2.txt', 'a+', encoding='utf-8') as f1:
                        f1.write(c_clean + '\t' + a[0] +'\n')
                else:
                    print('没有')
                    with open('企业简称名单_revise2.txt', 'a+', encoding='utf-8') as f1:
                        f1.write(c_clean +'\n')
                # myquery = {"url": url, "person_name":person_name}
                # newvalues = {"$set": {'company_full_name': a}}
                #
                # col1.update_one(myquery, newvalues)
                # print('修改成功')
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)
                # myquery = {"url": url, "person_name":person_name}
                # newvalues = {"$set": {'company_full_name': a}}
                #
                # col1.update_one(myquery, newvalues)
                # time.sleep(1)
