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

reload(sys)
sys.setdefaultencoding("utf-8")

# facebook spider
class Facebook:
    # init
    def __init__(self):
        # login url
        self.baseURL = 'https://facebook.com'
        self.headers = [
            "Host:www.facebook.com",
            "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent:Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
            "Referer:https://www.facebook.com/",
            "Content-Type:application/x-www-form-urlencoded",
            "Origin:https://www.facebook.com", "Upgrade-Insecure-Requests:1",
            "Accept-Language:zh-CN,zh;q=0.8", "Connection:Keep-Alive"
        ]

        self.receiveurl = ''
        self.id = ''

        # username
        self.email = ''
        self.password = ''

        self.cookies = ''
        self.postData = ''

        self.account_id = ''
        self.async_get_token = ''

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
            _file = open("result", 'ab')
            _file.write(formdata)
            _file.write(
                "\n====================================================\n")
            _file.close()
            #====================================================

            #time.sleep(1)
            #self.header_str.truncate(0)
            #self.response_str.truncate(0)
            #self.con.setopt(pycurl.POST, 1)
            #self.con.setopt(pycurl.HTTPHEADER, headers)
            #self.con.setopt(pycurl.POSTFIELDS, formdata)
            #self.con.setopt(pycurl.URL, self.receiveurl)
            #self.con.perform()
            #response = self.response_str.getvalue()
            #self.logger.info(response)

        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -sent data end- ###')

    # get first page
    def login_first_step(self):
        print('### -first step start- ###')
        sent_url = 'https://www.facebook.com'

        self.header_str.truncate(0)
        self.response_str.truncate(0)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()
        response = self.response_str.getvalue()

        datr = lsd = lgndim = lgnjs = lgnrnd = ''

        # find lsd
        reg = r'<input type="hidden" name="lsd" value="(.*?)" autocomplete="off" />'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            lsd = search.group(1)

        # find lgndim
        reg = r'<input type="hidden" autocomplete="off" name="lgndim" value="(.*?)"'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            lgndim = search.group(1)

        # find lgnrnd
        reg = r'<input type="hidden" name="lgnrnd" value="(.*?)" />'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            lgnrnd = search.group(1)

        # find lgnjs
        reg = r'<input type="hidden" id="lgnjs" name="lgnjs" value="(.*?)" />'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            lgnjs = search.group(1)

        # find datr
        reg = r'"_js_datr","(.*?)",'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            datr = search.group(1)

        # set cookies in step 2
        self.cookies = 'version=0,name=datr,value=' + datr + ',port=None,port_specified=False,domain=.facebook.com,domain_specified=True,domain_initial_dot=False,path=/,path_specified=True,secure=False,expires=None,discard=False,comment=None,comment_url=None,rest=None'

        # set post in step 2
        self.postData = 'lsd=' + lsd + '&email=' + self.email + '&pass=' + self.password + '&persistent=&default_persistent=1&timezone=&lgndim=&lgnrnd=' + lgnrnd + '&lgnjs=' + lgnjs + '&locale=zh_CN&next=https%3A%2F%2Fwww.facebook.com%2F'

        print('lsd:', lsd)
        print('lgndim:', lgndim)
        print('lgnjs:', lgnjs)
        print('lgnrnd:', lgnrnd)
        print('datr:', datr)

        print('### -first step end- ###')

    # get second page
    def login_second_step(self):
        print '### -second step start- ###'
        sent_url = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'

        self.header_str.truncate(0)
        self.response_str.truncate(0)

        self.con.setopt(pycurl.POST, 1)
        self.con.setopt(pycurl.COOKIE, self.cookies)
        self.con.setopt(pycurl.POSTFIELDS, self.postData)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()

        response = self.response_str.getvalue()

        print '### -second step end- ###'

    # get third page
    def login_third_step(self):
        print '### -thirt step start- ###'
        sent_url = 'https://www.facebook.com'

        self.header_str.truncate(0)
        self.response_str.truncate(0)

        self.con.setopt(pycurl.HTTPGET, 1)
        self.con.setopt(pycurl.HTTPHEADER, self.headers)
        self.con.setopt(pycurl.URL, sent_url)
        self.con.perform()

        response = self.response_str.getvalue()

        # find account_id
        reg = r'"USER_ID":"(.*?)","ACCOUNT_ID":"(.*?)"'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            self.account_id = search.group(1)

        # find async_get_token
        reg = r'"async_get_token":"(.*?)"'
        m = re.compile(reg)
        search = re.search(m, response)
        if search:
            self.async_get_token = search.group(1)

        print('account_id:', self.account_id)
        print('async_get_token:', self.async_get_token)

        print '### -thirt step end- ###'

    # login api
    def login_facebook(self):
        self.login_first_step()
        self.login_second_step()
        self.login_third_step()

    # get user_id
    def get_user_id(self, html):
        pattarn = re.compile('"USER_ID":"(.*?)","ACCOUNT_ID":"(.*?)"', re.S)
        result = re.search(pattarn, html)
        if result:
            print 'user_id is ' + result.group(1)
        else:
            print 'user_id is empty'
            return '-1'
        return result.group(1)

    # get async_get_token
    def get_async_get_token(self, html):
        pattern = re.compile('"async_get_token":"(.*?)"', re.S)
        result = re.search(pattern, html)
        if result:
            print 'async_get_token is ' + result.group(1)
        else:
            print 'async_get_token is empty'
            return '-1'
        return result.group(1)

    # get pagelet_token
    def get_pagelet_token(self, html):
        pattern = re.compile(
            'disablepager:false,overview:false,profile_id:(.*?)pagelet_token:"(.*?)"',
            re.S)
        result = re.search(pattern, html)
        if result:
            print 'pagelet_token is ' + result.group(2)
        else:
            print 'pagelet_token is empty'
            return '-1'
        return result.group(2)

    # get collection_token
    def get_collection_token(self, html):
        pattern = re.compile(
            '"root":true,"pagelet":"pagelet_timeline_app_collection_(.*?)".*?',
            re.S)
        result = re.search(pattern, html)
        if result:
            print 'collection_token is ' + result.group(1)
        else:
            print 'collection_token is empty'
            return '-1'
        return result.group(1)

    # get friends_lst
    def get_friends_lst(self, html):
        pattern = re.compile(
            '"root":true,"pagelet":"pagelet_timeline_app_collection_(.*?)".*?',
            re.S)
        result = re.search(pattern, html)
        if result:
            print 'friends_lst is ' + result.group(1)
        else:
            print 'friends_lst is empty'
            return '-1'
        return result.group(1)

    # get page_cursor first
    def get_page_cursor_first(self, html):
        #pattarn = re.compile('"TimelineAppCollection","enableContentLoader".*?__m:".*?"},"(.*?)"]', re.S)
        pattarn = re.compile(
            'elements:.*?enableContentLoader.*?__m:"__elem_.*?"},"(.*?)"',
            re.S)
        result = re.search(pattarn, html)
        if result:
            print 'page_cursor is ' + result.group(1)
        else:
            print 'page_cursor is empty'
            return '-1'
        return result.group(1)

    # get page_cursor
    def get_page_cursor(self, html):
        pattarn = re.compile('"elements":.*?"__m":"__elem_.*?"},"(.*?)"', re.S)
        result = re.search(pattarn, html)
        if result:
            print 'page_cursor is ' + result.group(1)
        else:
            print 'page_cursor is empty'
            return '-1'
        return result.group(1)

    # get ajaxpipe_token
    def get_ajaxpipe_token(self, html):
        pattern = re.compile('{"ajaxpipe_token":"(.*?)",.*?', re.S)
        result = re.search(pattern, html)
        if result:
            print 'ajaxpipe_token is ' + result.group(1)
        else:
            print 'ajaxpipe_token is empty'
            return '-1'
        return result.group(1)

    # get image
    def get_image(self, url, value):
        self.logger.info('### -get image start- ###')
        try:
            data_dict = {}
            sent_url = HTMLParser.HTMLParser().unescape(url)
            headers = [
                "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "User-Agent:Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                "Referer:https://www.facebook.com/",
                "Content-Type:application/x-www-form-urlencoded",
                "Upgrade-Insecure-Requests:1",
                "Accept-Language:zh-CN,zh;q=0.8", "Connection:Keep-Alive"
            ]

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
        finally:
            self.logger.info('### -get user timelines end- ###')

    # analysis user information
    def analysis_user_information(self, html):
        print '---------------analysis user information start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        # uri and username
        pattern = re.compile('<a class="_2nlw _2nlv" href="(.*?)">(.*?)<',
                             re.S)
        result = re.search(pattern, content)
        url = result.group(1)
        name = result.group(2)
        self.name = name

        # avatar_url
        pattern = re.compile('<img class="_11kf img".*?src="(.*?)" />', re.S)
        result = re.search(pattern, content)
        avatar_url = HTMLParser.HTMLParser().unescape(result.group(1))

        # area
        pattern = re.compile(
            '<div class="_50f3">.*?<a class="profileLink".*?>(.*?)</a></div>',
            re.S)
        result = re.search(pattern, content)
        if result:
            area = result
        else:
            area = ''
        formdata = {
            'index': 'social_platform',
            'type': 'facebook',
            'id': self.id,
            'user_id': self.id,
            'nickname': name,
            'url': url,
            'location': area
        }
        avatar = self.get_image(avatar_url, "icon")
        formdata = dict(formdata, **avatar)
        self.send_data(formdata)
        print '---------------analysis user information end----------------'

    # get user information
    def get_user_information(self):
        try:
            print '--------------get user information start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&id=' + self.id
            response = self.get_response(sent_url)
            self.analysis_user_information(response)
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user information end- ###')

    # analysis user friends
    def analysis_user_friends(self, html):
        print '---------------analysis user friends start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        pattern = re.compile('<li class="_698">.*?</li>', re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                '<a class="_5q6s _8o _8t lfloat _ohe" href="(.*?)" .*?>.*?</a>.*?<a .*?data-hovercard-prefer-more-content-show="1">(.*?)</a>.*?data-profileid="(.*?)"',
                re.S)
            result = re.search(pattern, item)
            if result:
                url = HTMLParser.HTMLParser().unescape(result.group(1).strip())
                name = result.group(2).strip()
                user_id = result.group(3).strip()
                formdata = {
                    'index': 'social_platform',
                    'type': 'facebook',
                    'id': user_id,
                    'user_id': user_id,
                    'nickname': name,
                    'url': url,
                }
                self.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'friends',
                }
                self.send_data(formdata)
        print '---------------analysis user friends end----------------'

    # get user friends
    def get_user_friends(self):
        try:
            print '---------------get user friends start----------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&sk=friends&source_ref=pb_friends_tl&id=' + self.id

            response = self.get_response(sent_url)

            fb_dtsg_ag = ''
            profile_id = self.id
            __user = self.account_id
            lst = self.get_friends_lst(response)
            pagelet_token = self.get_pagelet_token(response)
            collection_token = self.get_collection_token(response)
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(response)
            else:
                fb_dtsg_ag = self.async_get_token
            cursor = self.get_page_cursor_first(response)
            while True:
                self.analysis_user_friends(response)
                if cursor == '-1' or cursor == 'ARS':
                    break
                # get more friends
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                print 'sent_url : ' + sent_url
                response = self.get_response(sent_url)
                cursor = self.get_page_cursor(response)
            print '---------------get user friends end------------------'
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user friends end- ###')

    # analysis user followers
    def analysis_user_followers(self, html):
        print '---------------analysis user followers start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        pattern = re.compile('<li class="fbProfileBrowserListItem">.*?</li>',
                             re.S)
        items = re.findall(pattern, content)
        for item in items:
            # print item
            pattern = re.compile(
                '<a class="_8o _8t lfloat _ohe" href="(.*?)" .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?data-profileid="(.*?)"',
                re.S)
            result = re.search(pattern, item)
            if result:
                url = HTMLParser.HTMLParser().unescape(result.group(1).strip())
                name = result.group(2).strip()
                user_id = result.group(3).strip()
                formdata = {
                    'index': 'social_platform',
                    'type': 'facebook',
                    'id': self.id,
                    'user_id': user_id,
                    'nickname': name,
                    'url': url,
                }
                self.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'followers',
                }
                self.send_data(formdata)
        print '---------------analysis user followers end----------------'

    # get user followers
    def get_user_followers(self):
        try:
            print '--------------get user followers start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&sk=followers&source_ref=pb_friends_tl&id=' + self.id
            response = self.get_response(sent_url)
            #result = self.analysis_user_followers(html)

            collection_token = self.get_collection_token(response)
            pagelet_token = self.get_pagelet_token(response)
            fb_dtsg_ag = self.get_async_get_token(response)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(response)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(response)
            profile_id = self.id
            cursor = self.get_page_cursor_first(response)
            while True:
                self.analysis_user_followers(response)
                if cursor == '-1' or cursor == 'interaction_boost':
                    break
                # get more friends
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/FollowersAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                response = self.get_response(sent_url)
                cursor = self.get_page_cursor(response)
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user followers end- ###')

    # analysis user like
    def analysis_user_likes(self, html):
        print '---------------analysis user like start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        pattern = re.compile('<li class="_5rz _5k3a _5rz3 _153f">.*?</li>',
                             re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                '<a class="_8o _8t lfloat _ohe" href="(.*?)" .*?>.*?<img class=".*?" src="(.*?)".*?</a>.*?<a .*?>(.*?)</a>.*?<div class="fsm fwn fcg">(.*?)</div>.*?data-profileid="(.*?)"',
                re.S)
            result = re.search(pattern, item)
            if result:
                url = HTMLParser.HTMLParser().unescape(result.group(1).strip())
                avatar_url = HTMLParser.HTMLParser().unescape(result.group(2).strip())
                name = result.group(3).strip()
                nature = result.group(4).strip()
                user_id = result.group(5).strip()
                formdata = {
                    'index': 'social_platform',
                    'type': 'facebook',
                    'id': user_id,
                    'user_id': user_id,
                    'nature' : nature,
                    'nickname': name,
                    'url': url,
                }
                avatar = self.get_image(avatar_url, "icon")
                formdata = dict(formdata, **avatar)
                self.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'like',
                }
                self.send_data(formdata)
        print '---------------analysis user like end----------------'

    # get user likes
    def get_user_likes(self):
        try:
            print '--------------get user likes start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&&sk=likes&id=' + self.id
            response = self.get_response(sent_url)
            #result = self.analysis_user_likes(html)

            collection_token = self.get_collection_token(response)
            pagelet_token = self.get_pagelet_token(response)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(response)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(response)
            profile_id = self.id
            cursor = self.get_page_cursor_first(response)
            while True:
                self.analysis_user_likes(response)
                if cursor == '-1' or cursor == '277509099012208':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/LikesWithFollowCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                response = self.get_response(sent_url)
                cursor = self.get_page_cursor(response)
            print '---------------get user likes end----------------'
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user timelines end- ###')

    # analysis user photos
    def analysis_user_photos(self, html):
        print '---------------analysis user photos start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        pattern = re.compile(
            '<li class="fbPhotoStarGridElement fbPhotoStarGridNonStarred focus_target _53s fbPhotoCurationControlWrapper" data-starred-src=".*?".*?>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(' data-starred-src="(.*?)" ', re.S)
            result = re.search(pattern, item)
            if result:
                photo_url = HTMLParser.HTMLParser().unescape(
                    result.group(1).strip())
                print 'photo_url:\n' + photo_url
                formdata = {
                    'index': 'social_platform',
                    'type': 'facebook',
                    'id': self.id,
                    'timestamp': 'timestamp',
                }
                photo = self.get_image(photo_url, "photo")
                formdata = dict(formdata, **photo)
                self.send_data(formdata)
        print '---------------analysis user photos end----------------'

    # get user photos
    def get_user_photos(self):
        try:
            print '--------------get user photos start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&&sk=photos&id=' + self.id
            response = self.get_response(sent_url)

            collection_token = self.get_collection_token(response)
            pagelet_token = self.get_pagelet_token(response)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(response)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(response)
            profile_id = self.id
            cursor = self.get_page_cursor_first(response)
            while True:
                self.analysis_user_photos(response)
                if cursor == '-1':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/TaggedPhotosAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                response = self.get_response(sent_url)
                cursor = self.get_page_cursor(response)
            print '---------------get user photos end----------------'
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user photos end- ###')

    # get data_first
    def get_data_first(self, html):
        #print html
        pattern = re.compile(
            '"ProfileTimelineSectionPagelet",{profile_id:(.*?),start:(.*?),end:(.*?),.*?lst:"(.*?)",buffer:(.*?),.*?page_index:(.*?),.*?tipld:{sc:(.*?),vc:(.*?)},num_visible_units:(.*?),.*?pagelet_token:"(.*?)"}',
            re.S)
        result = re.search(pattern, html)
        if result:
            profile_id = result.group(1)
            start = result.group(2)
            end = result.group(3)
            lst = result.group(4)
            buffer = result.group(5)
            page_index = result.group(6)
            sc = result.group(7)
            vc = result.group(8)
            num_visible_units = result.group(9)
            pagelet_token = result.group(10)
            data = '{"profile_id":' + profile_id + ',"start":' + start + ',"end":' + end + ',"query_type":36,"sk":"timeline","lst":"' + lst + '","buffer":' + buffer + ',"current_scrubber_key":"recent","page_index":' + page_index + ',"require_click":false,"section_container_id":"u_0_1j","section_pagelet_id":"pagelet_timeline_recent","unit_container_id":"u_0_1i","showing_esc":false,"tipld":{"sc":' + sc + ',"vc":' + vc + '},"num_visible_units":' + num_visible_units + ',"remove_dupes":true,"pagelet_token":"' + pagelet_token + '"}'

            print 'data is ' + data
        else:
            print 'data is empty'
            return '-1'
        return data

    # get data
    def get_data(self, html):
        pattern = re.compile(
            '"ProfileTimelineSectionPagelet",{"profile_id":(.*?),"start":(.*?),"end":(.*?),.*?"lst":"(.*?)","buffer":(.*?),.*?"page_index":(.*?),.*?"tipld":{"sc":(.*?),"vc":(.*?)},"num_visible_units":(.*?),.*?"pagelet_token":"(.*?)"}',
            re.S)
        result = re.search(pattern, html)
        if result:
            profile_id = result.group(1)
            start = result.group(2)
            end = result.group(3)
            lst = result.group(4)
            buffer = result.group(5)
            page_index = result.group(6)
            sc = result.group(7)
            vc = result.group(8)
            num_visible_units = result.group(9)
            pagelet_token = result.group(10)
            data = '{"profile_id":' + profile_id + ',"start":' + start + ',"end":' + end + ',"query_type":36,"sk":"timeline","lst":"' + lst + '","buffer":' + buffer + ',"current_scrubber_key":"recent","page_index":' + page_index + ',"require_click":false,"section_container_id":"u_0_1j","section_pagelet_id":"pagelet_timeline_recent","unit_container_id":"u_0_1i","showing_esc":false,"tipld":{"sc":' + sc + ',"vc":' + vc + '},"num_visible_units":' + num_visible_units + ',"remove_dupes":true,"pagelet_token":"' + pagelet_token + '"}'

            print 'data is ' + data
        else:
            print 'data is empty'
            return '-1'
        return data

    # analysis user timelines
    def analysis_user_timelines(self, html):
        print '---------------analysis user timelines start----------------'
        content = unquote(html).encode().decode('unicode_escape').replace(
            '&quot;', '"').replace('\\', '')
        pattern = re.compile(
            '<div class="_1dwg _1w_m _q7o">.*?<div><form rel="async"', re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-utime="(.*?)".*?<p>(.*?)<',
                re.S)
            result = re.search(pattern, item)
            if result:
                timestamp = result.group(1)
                remark = result.group(2)
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'facebook',
                    'id': self.id + '_' + timestamp, 
                    'user_id': self.id,
                    'nickname': self.id,
                    'timestamp': timestamp.encode('utf-8'),
                    'content': remark.encode('utf-8'),
                }
                self.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + timestamp,
                    'source': self.id,
                    'target_content': timestamp,
                    'content_relation': 'send',
                }
        print '---------------analysis user timelines end----------------'


    # get user timelines
    def get_user_timelines(self):
        try:
            print '--------------get user timelines start---------------'
            sent_url = 'https://www.facebook.com/profile.php?id=' + self.id
            response = self.get_response(sent_url)
            __user = self.account_id
            ajaxpipe_token = self.get_ajaxpipe_token(response)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(response)
            else:
                fb_dtsg_ag = self.async_get_token
            data = self.get_data_first(response)
            while True:
                self.analysis_user_timelines(response)
                if data == '-1':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/ProfileTimelineSectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&ajaxpipe=1&ajaxpipe_token=' + ajaxpipe_token + '&no_script_path=1&data=' + data + '&__user=' + __user + '&__a=1&__req=fetchstream_4&__be=1&__pc=PHASED:DEFAULT&__rev=4418982&__spin_r=4418982&__spin_b=trunk&__spin_t=1539525330&__adt=4&ajaxpipe_fetch_stream=1'
                response = self.get_response(sent_url)
                data = self.get_data(response)
        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('### -get user timelines end- ###')


    def run(self, target, module, email, password, receiveurl):
        try:
            self.logger.info("Crawl start(%s),Crawl module is facebook %s" % (time.ctime(time.time()), module))

            self.id = target
            self.email = email
            self.password = password
            self.receiveurl = receiveurl

            if self.login_facebook():
                raise Exception, "login facebook faild!"
                
            if module == "information":
                self.get_user_information()

            if module == "friends":
                self.get_user_friends()

            if module == "followers":
                self.get_user_followers()

            if module == "photos":
                self.get_user_photos()

            if module == "likes":
                self.get_user_likes()

            if module == "timelines":
                self.get_user_timelines()

        except Exception, e:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info("End of crawl(%s)" % (time.ctime(time.time())))


# facebook data entry

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'The parameters are incorrect, please check the parameters.'
        exit()

    # target 目标ID
    # module 目标模块
    # email 爬虫配置账号
    # password 爬虫配置密码
    # receiveurl 服务器回连地址

    target = sys.argv[1]
    module = sys.argv[2]
    email = sys.argv[3]
    password = sys.argv[4]
    receiveurl = sys.argv[5]

    facebook = Facebook()
    facebook.run(target, module, email, password, receiveurl)
