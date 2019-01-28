#!/usr/bin/env python
# -- coding: utf-8 --

import os
import time
import urllib
import urllib2
import cookielib
import json
import base64
import re
import sys
import chardet
import HTMLParser
import traceback
import logging
import pycurl
import StringIO
import types

from urllib import unquote
from lxml import etree
from logging import config
from logging import handlers
from types import *

reload(sys)
sys.setdefaultencoding("utf-8")


# twitter spider
class Twitter:
    # init
    def __init__(self):
        # login url
        self.baseURL = 'https://twitter.com'
        self.headers = [
            "Host:twitter.com",
            "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent:Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
            "Referer:https://twitter.com/",
            "Content-Type:application/x-www-form-urlencoded",
            "Origin:https://twitter.com", "Upgrade-Insecure-Requests:1",
            "Accept-Language:zh-CN,zh;q=0.8", "Connection:Keep-Alive"
        ]

        self.myfunction = {
            "get_id": self.get_id,
            "get_value": self.get_value,
            "catenate_id": self.catenate_id
        }

        self.receiveurl = ''
        self.id = ''

        # username
        self.email = ''
        self.password = ''
        self.postData = ''
        self.authenticity_token = ''
        self.a = ''
        self.b = ''
        self.c = ''
        self.d = ''
        self.s = ''

        self.header_str = StringIO.StringIO()
        self.response_str = StringIO.StringIO()

        self.con = pycurl.Curl()
        #设置cookie
        self.con.setopt(pycurl.COOKIEFILE, "cookie")  #把cookie保存在该文件中
        self.con.setopt(pycurl.COOKIEJAR, "cookie")  #从该文件中读取cookie
        #设置跳转
        self.con.setopt(pycurl.FOLLOWLOCATION, 1)  #遇到302时候是否进行自动跳转
        self.con.setopt(pycurl.MAXREDIRS, 5)  #网页最多跳转的次数
        #设置SSL
        self.con.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.con.setopt(pycurl.SSL_VERIFYHOST, 0)
        #设置超时
        self.con.setopt(pycurl.CONNECTTIMEOUT, 10)  #设置链接超时
        self.con.setopt(pycurl.TIMEOUT, 20)  #设置下载超时
        #设置回写数据
        self.con.setopt(pycurl.HEADERFUNCTION, self.header_str.write)
        self.con.setopt(pycurl.WRITEFUNCTION, self.response_str.write)

        # 读取日志配置文件内容
        logging.config.fileConfig('logging.conf')

        # 创建一个日志器logger
        self.logger = logging.getLogger('spider')

    def get_id(self, value, data):
        return self.id

    def get_value(self, value, data):
        return data[value]

    def catenate_id(self, value, data):
        return self.id + "_" + data[value]

    # get first page
    def login_first_step(self):
        self.logger.info('### -first step start- ###')
        sent_url = 'https://twitter.com'

        self.header_str.truncate(0)
        self.response_str.truncate(0)

        self.con.setopt(pycurl.HTTPGET, 1)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()

        response = self.response_str.getvalue()

        pattern = re.compile(
            '<input type="hidden" value="(.*?)" name="authenticity_token">',
            re.S)
        result = re.search(pattern, response)
        if result:
            self.authenticity_token = result.group(1)
        else:
            self.authenticity_token = '-1'

        self.logger.info(self.authenticity_token)
        self.logger.info('### -first step end- ###')

    # get second page
    def login_second_step(self):
        self.logger.info('### -second step start- ###')
        sent_url = 'https://twitter.com/i/js_inst?c_name=ui_metrics'

        self.header_str.truncate(0)
        self.response_str.truncate(0)

        self.con.setopt(pycurl.HTTPGET, 1)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()

        response = self.response_str.getvalue()

        pattern = re.compile("'rf':(.*?);", re.S)
        result = re.search(pattern, response)
        rf = ''
        if result:
            rf = result.group(1)
        pattern = re.compile(
            "{'(.*?)':.*?,'(.*?)':.*?,'(.*?)':.*?,'(.*?)':.*?,'s':'(.*?)'}")
        result = re.search(pattern, rf)
        if result:
            self.a = result.group(1)
            self.b = result.group(2)
            self.c = result.group(3)
            self.d = result.group(4)
            self.s = result.group(5)
            self.logger.info(self.a)
            self.logger.info(self.b)
            self.logger.info(self.c)
            self.logger.info(self.d)
            self.logger.info(self.s)
        self.logger.info('### -second step end- ###')

    # get third page
    def login_third_step(self):
        self.logger.info('### -thirt step start- ###')
        self.postData = 'session[username_or_email]=%s&session[password]=%s&return_to_ssl=true&scribe_log=&redirect_after_login=/&authenticity_token=%s&ui_metrics={"rf":{"%s":-129,"%s":-143,"%s":-33,"%s":-44},"s":"%s"}' % (
            self.email, self.password, self.authenticity_token, self.a, self.b,
            self.c, self.d, self.s)

        sent_url = 'https://twitter.com/sessions'

        self.header_str.truncate(0)
        self.response_str.truncate(0)

        self.con.setopt(pycurl.POST, 1)
        self.con.setopt(pycurl.POSTFIELDS, self.postData)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()

        response = self.response_str.getvalue()
        self.logger.info('### -thirt step end- ###')

    # login api
    def login_twitter(self):
        self.login_first_step()
        self.login_second_step()
        self.login_third_step()

    # sent data
    def send_data(self, data):
        try:
            self.logger.info('### -sent data start- ###')
            headers = [
                'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                'Content-Type:application/x-www-form-urlencoded',
                'Accept-Language:zh-CN,zh;q=0.8', 'Connection:Keep-Alive'
            ]
            formdata = urllib.urlencode(data)
            #====================================================
            # _file = open("result", 'ab')
            # _file.write(formdata)
            # _file.write(
            #     "\n====================================================\n")
            # _file.close()
            #====================================================

            time.sleep(1)

            self.header_str.truncate(0)
            self.response_str.truncate(0)
            self.con.setopt(pycurl.POST, 1)
            self.con.setopt(pycurl.HTTPHEADER, headers)
            self.con.setopt(pycurl.POSTFIELDS, formdata)
            self.con.setopt(pycurl.URL, self.receiveurl)
            self.con.perform()
            response = self.response_str.getvalue()
            self.logger.info(response)

        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -sent data end- ###')

    # get image
    def get_image(self, value, url):
        self.logger.info('### -get image start- ###')
        try:
            data_dict = {}
            sent_url = HTMLParser.HTMLParser().unescape(url)
            headers = [
                "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "User-Agent:Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                "Referer:https://twitter.com/",
                "Content-Type:application/x-www-form-urlencoded",
                "Upgrade-Insecure-Requests:1",
                "Accept-Language:zh-CN,zh;q=0.8", "Connection:Keep-Alive"
            ]

            self.logger.info(value)
            self.logger.info(sent_url)

            self.header_str.truncate(0)
            self.response_str.truncate(0)

            self.con.setopt(pycurl.HTTPGET, 1)
            self.con.setopt(pycurl.HTTPHEADER, headers)
            self.con.setopt(pycurl.URL, sent_url)
            self.con.perform()

            header = self.header_str.getvalue()
            response = self.response_str.getvalue()

            HttpCode = self.con.getinfo(self.con.HTTP_CODE)
            ContentType = self.con.getinfo(self.con.CONTENT_TYPE)

            if HttpCode != 200:
                self.logger.error(("code:%d ") % (HttpCode))
                self.logger.error(("response:%s ") % (response))
                raise Exception, ("get image error! httpcode:%d ") % (HttpCode)

            imgData = base64.b64encode(response)
            data_dict[value + '_type'] = ContentType
            data_dict[value] = imgData

            return data_dict
        except Exception, e:
            self.logger.error(traceback.format_exc())
            return {}
        finally:
            self.logger.info('### -get image end- ###')

    # get response
    def get_response(self, sent_url):
        try:
            self.logger.info('### -get response start- ###')

            self.header_str.truncate(0)
            self.response_str.truncate(0)

            self.con.setopt(pycurl.HTTPHEADER, self.headers)
            self.con.setopt(pycurl.URL, sent_url)
            self.con.perform()

            response = self.response_str.getvalue()

            return response
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get response end- ###')

    # analysis
    def analysis_parameter(self, html, rule):
        try:
            self.logger.info('### -analysis parameter start- ###')
            data_dict = {}
            for key, value in rule.items():
                data = ''.join(html.xpath(value))
                if data != "":
                    data_dict[key] = data
            return data_dict
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -analysis parameter end- ###')

    # analysis
    def analysis_data(self, html, rule):
        try:
            self.logger.info('### -analysis data start- ###')
            data_dict = {}
            Regular = rule.get("Regular")
            for key in Regular.keys():
                value = Regular.get(key)
                if isinstance(value, dict):
                    data = html.xpath(key)
                    if isinstance(data, list):
                        for array in data:
                            temp_dict = self.analysis_data(array, value)
                            if isinstance(temp_dict, dict):
                                data_dict = dict(data_dict, **temp_dict)
                else:
                    data = ''.join(html.xpath(key))
                    if data != "":
                        if '_url' in value:
                            avatar = self.get_image(
                                value.replace('_url', ''), data)
                            data_dict = dict(data_dict, **avatar)
                        else:
                            data_dict[value] = data

            if rule.get("root"):
                index = rule.get("index")
                if index:
                    temp_dict = {}
                    for key, value in index.items():
                        if isinstance(value, dict):
                            temp_dict[key] = self.myfunction[value["method"]](
                                value["value"], data_dict)
                        else:
                            temp_dict[key] = value
                    data_dict = dict(data_dict, **temp_dict)
                    self.send_data(data_dict)

                relation = rule.get("relation")
                if relation:
                    formdata = {}
                    for key, value in relation.items():
                        if isinstance(value, dict):
                            formdata[key] = self.myfunction[value["method"]](
                                value["value"], data_dict)
                        else:
                            formdata[key] = value
                    self.send_data(formdata)

                return ""
            else:
                return data_dict
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -analysis data end- ###')

    # analysis
    def analysis_rule(self, rule, parameter):
        self.logger.info('### -analysis rule start- ###')
        try:
            if not (isinstance(rule, dict) and rule):
                raise Exception, "Rule error!"

            parameter_rule = rule.get("parameter")
            data_rule = rule.get("data")
            data_type = rule.get("type")
            url = rule.get("url")
            node_next = rule.get("next")
            new_parameter = {}

            if isinstance(parameter, dict) and parameter:
                url = url.replace('<min_position>', parameter["min_position"])

            url = url.replace('<userid>', self.id)

            response = self.get_response(url)

            if response == "":
                raise Exception, "Failed to get response data!"

            if data_type == "json":
                jsondata = json.loads(response)
                response = jsondata["items_html"]
                html = etree.HTML(
                    response.replace('\\n', '').replace('\n', ''))
                new_parameter["min_position"] = jsondata["min_position"]
                if parameter and (new_parameter["min_position"] ==
                                  parameter["min_position"]):
                    new_parameter = ""
            elif data_type == "html":
                html = etree.HTML(response.replace('\\n', '').replace('\n', ''))
                new_parameter = self.analysis_parameter(html, parameter_rule)

            if html is not None:
            #if type(html) is not NoneType:
                self.analysis_data(html, data_rule)

            if node_next:
                node_rule = rule.get("node")
                if not (isinstance(node_rule, dict) and node_rule):
                    raise Exception, "node Rule error!"
                while ((isinstance(new_parameter, dict))
                       and (new_parameter.get("min_position"))
                       and (new_parameter["min_position"] != "0")):
                    new_parameter = self.analysis_rule(node_rule,
                                                       new_parameter)
            else:
                return new_parameter

        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -analysis rule end- ###')

    def run(self, target, module, email, password, receiveurl):
        try:
            self.logger.info("Crawl start(%s),Crawl module is twitter %s" %
                             (time.ctime(time.time()), module))

            self.id = target
            self.email = email
            self.password = password
            self.receiveurl = receiveurl
            # if self.login_twitter():
            #       raise Exception,"Invalid level!"

            all_rule = json.load(open("rule_twitter.json", 'r'))
            module_rule = all_rule.get(module)
            if module_rule:
                self.analysis_rule(module_rule, "")
            else:
                raise Exception, ("Target module does not exist,The incoming module is %s" % module)

        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info("End of crawl(%s)" % (time.ctime(time.time())))


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print('The parameters are incorrect, please check the parameters.')
        exit()

    # target 目标ID
    # module 目标模块
    # email 爬虫配置账号
    # password 爬虫配置密码
    # receive_url 服务器回连地址

    target = sys.argv[1]
    module = sys.argv[2]
    email = sys.argv[3]
    password = sys.argv[4]
    receiveurl = sys.argv[5]

    twitter = Twitter()
    twitter.run(target, module, email, password, receiveurl)
