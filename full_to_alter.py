import json
# import pymysql
import logging
import re
import copy
import os
import requests
from bs4 import BeautifulSoup
import collections
import time

logger = logging.getLogger(__name__)
cur_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(cur_path, "candidate.json")

class AlternameProcessor(object):

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
            'Host': 'www.baidu.com',
        }


    def run_find_simple_name(self, name):
        logger.info('Begin Run')
        simple_name_list = []
        
        url = 'http://www.baidu.com/s?lm=0&si=&rn=40&ie=gbk&ct=0%20&wd=' + name + '&pn=10' + '&ver=0&cl=3&uim=6&usm=0'
        # url = 'http://www.baidu.com/s?wd='+name+'&pn=30&usm=3&rsv_idx=2&rsv_page=1'
        # resp = requests.get(url, headers)
        resp = requests.get(url, self.headers)
        if resp:
            resp.encoding = 'utf-8'
            content = resp.text

            soup = BeautifulSoup(content, 'lxml')
            tag_list = soup.find_all('em')
            if tag_list:
                for i in tag_list:
                    i_text = i.get_text().strip()
                    # print(i_text)
                    simple_name_list.append(i_text)
            else:
                # print('No tag_list')
                logger.info('No tag_list')

            # print(simple_name_list)
            content_linshi = []
            simple_name_list_linshi = []
            if simple_name_list:
                tag1 = simple_name_list[0]
                tag2 = simple_name_list[1:]
                for i2 in simple_name_list:
                    if len(i2) > 2:
                        if tag1 == tag2:
                            continue
                        elif ('有限公司' in i2) or ('有限责任公司' in i2):
                            continue
                        elif '集团公司' == i2 or '公司' == i2 or '股份公司' == i2:
                            continue
                        elif ('市' in i2) or ('省' in i2) or ('县' in i2):
                            continue
                        # print(i2)
                        simple_name_list_linshi.append(i2)

                if simple_name_list_linshi:
                    # TODO 开始反向搜索
                    col_counter = collections.Counter(simple_name_list_linshi)
                    # print(col_counter)
                    list_c1 = []
                    if col_counter:
                        # c1 = 0
                        for key, value in col_counter.items():
                            # print(value)
                            list_c1.append(value)
                            # print(list_c1)
                        list_c1.sort(reverse=True)
    
                    # print(list_c1)
                    # print(list_c1[0])

                    # TODO 统计出频率最高的简称
                    c2 = [k for k, v in col_counter.items() if v == list_c1[0]]
                    print('c2:', c2)

                    # TODO 开始验证最高频率简称
                    list_keys = col_counter.keys()
                    if c2:
                        flag, list_word = self.backward_search(c2, tag1)
                        if flag == 1:
                            for each in list_word:
                                content_linshi.append(each)
    
                            # print('有效简称')
                            logger.info("%s,%s,%s,%s" % (tag1, c2, list_word, '有效简称'))
                            # print('\n')
                            # return content_linshi
    
                        elif flag == 0:
                            flag, list_word = self.backward_search(list_keys, tag1)
                            if flag == 1:
                                for each in list_word:
                                    content_linshi.append(each)
                                # print('有效简称')
                                logger.info("%s,%s,%s,%s" % (tag1, c2, list_word, '有效简称'))
                                # return content_linshi
                            else:
                                # print('没有找到，无效简称')
                                logger.info("%s,%s,%s,%s" % (tag1, c2, list_word, '无效简称'))
                                # return content_linshi
                    else:
                        # print('没有找到，无效简称')
                        logger.info("%s,%s,%s" % (tag1, c2, '没有找到，无效简称，而且没有c2'))
            return content_linshi
        time.sleep(1)

    # 反向搜索
    def backward_search(self, c2, tag1):
        time.sleep(1.3)
        flag = 0
        list_word = []
        for each in c2:
            url = 'http://www.baidu.com/s?lm=0&si=&rn=40&ie=gbk&ct=0%20&wd=%' + each + '&pn=10' + '&ver=0&cl=3&uim=6&usm=0'
            resp = requests.get(url, self.headers)
            resp.encoding = 'utf-8'
            content = resp.text
            if tag1 in content:
                flag = 1
                list_word.append(each)
        return flag, list_word



if __name__ == "__main__":
    name = "杭州海康威视有限公司"
    p = AlternameProcessor()
    print(p.run_find_simple_name(name))





        

    





        
        


        