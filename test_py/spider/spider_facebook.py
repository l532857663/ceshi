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

from urllib import unquote

reload(sys)
sys.setdefaultencoding('UTF-8')


def print_ts(message):
    print "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                       message)


# get task
class Task:
    # init
    def __init__(self, url):
        # url
        self.headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }
        self.url = url
        self.postData = ''
        self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            self.httpHandler, self.httpsHandler,
            urllib2.HTTPCookieProcessor(self.cookies))

    # get id
    def get_id(self):
        try:
            sent_url = 'http://192.168.11.12:8080/get_task.php'
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            fbid = content.read()
            print 'The Facebook ID for this task is' + fbid
            return fbid
        except Exception, e:
            traceback.print_exc()
            print e
            return '-1'

    # sent data
    def send_data(self, formdata):
        try:
            headers = {
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                'Content-Type':
                'application/x-www-form-urlencoded',
                'Upgrade-Insecure-Requests':
                '1',
                'Accept-Language':
                'zh-CN,zh;q=0.8',
                'Connection':
                'Keep-Alive'
            }
            data = urllib.urlencode(formdata)
            request = urllib2.Request(url=self.url, headers=headers, data=data)
            content = self.opener.open(request)
            html = content.read()
            print html
        except Exception, e:
            traceback.print_exc()
            print e


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print('############ GOT 302 ###############')
        cookiemap = {}
        setcookie = str(headers["Set-Cookie"])
        cookieTokens = [
            "Domain", "Expires", "Path", "Max-Age", 'path', 'domain'
        ]
        tokens = setcookie.split(";")
        for cookie in tokens:
            cookie = cookie.strip()
            if cookie.startswith("Expires="):
                cookies = cookie.split(",", 2)
                if len(cookies) > 2:
                    cookie = cookies[2]
                    cookie = cookie.strip()
            else:
                cookies = cookie.split(",", 1)
                if len(cookies) > 1:
                    cookie = cookies[1]
                    cookie = cookie.strip()
            namevalue = cookie.split("=", 1)
            if len(namevalue) > 1:
                name = namevalue[0]
                value = namevalue[1]
                if name not in cookieTokens:
                    cookiemap[name] = value
        # print cookiemap
        str_cookie = ''
        for key in cookiemap:
            str_cookie = str_cookie + key + '=' + cookiemap[key] + '; '
        str_cookie = str_cookie[:-2]
        # print str_cookie
        req.add_header("Cookie", str_cookie)
        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)


# facebook spider
class Facebook:
    # init
    def __init__(self, url):
        # login url
        self.baseURL = 'https://www.facebook.com'
        self.headers = {
            'Host':
            'www.facebook.com',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer':
            'https://www.facebook.com/',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Origin':
            'https://www.facebook.com',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }

        self.task = Task(url)
        self.id = ''
        self.name = ''

        # username
        self.email = ''
        self.password = ''
        self.postData = ''
        self.account_id = ''
        self.async_get_token = ''
        self.cookies = cookielib.CookieJar()
        self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
        self.opener = urllib2.build_opener(
            self.httpHandler, self.httpsHandler, RedirectHandler,
            urllib2.HTTPCookieProcessor(self.cookies))

    # get first page
    def login_first_step(self):
        print('---------------first step start---------------')
        sent_url = 'https://www.facebook.com'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        content = self.opener.open(request)
        html = content.read()
        # print html
        datr = lsd = lgndim = lgnjs = lgnrnd = ''

        # find lsd
        reg = r'<input type="hidden" name="lsd" value="(.*?)" autocomplete="off" />'
        m = re.compile(reg)
        search = re.search(m, html)
        if search:
            lsd = search.group(1)

        # find lgndim
        reg = r'<input type="hidden" autocomplete="off" name="lgndim" value="(.*?)"'
        m = re.compile(reg)
        search = re.search(m, html)
        if search:
            lgndim = search.group(1)

        # find lgnrnd
        reg = r'<input type="hidden" name="lgnrnd" value="(.*?)" />'
        m = re.compile(reg)
        search = re.search(m, html)
        if search:
            lgnrnd = search.group(1)

        # find lgnjs
        reg = r'<input type="hidden" id="lgnjs" name="lgnjs" value="(.*?)" />'
        m = re.compile(reg)
        search = re.search(m, html)
        if search:
            lgnjs = search.group(1)

        # find datr
        reg = r'"_js_datr","(.*?)",'
        m = re.compile(reg)
        search = re.search(m, html)
        if search:
            datr = search.group(1)

        self.cookies.set_cookie(
            cookielib.Cookie(
                version=0,
                name='datr',
                value=datr,
                port=None,
                port_specified=False,
                domain=".facebook.com",
                domain_specified=True,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=False,
                expires=None,
                discard=False,
                comment=None,
                comment_url=None,
                rest=None))

        # set post in step 2
        self.postData = 'lsd=' + lsd + '&email=' + self.email + '&pass=' + self.password + '&persistent=&default_persistent=1&timezone=&lgndim=&lgnrnd=' + lgnrnd + '&lgnjs=' + lgnjs + '&locale=zh_CN&next=https%3A%2F%2Fwww.facebook.com%2F'

        print('lsd:', lsd)
        print('lgndim:', lgndim)
        print('lgnjs:', lgnjs)
        print('lgnrnd:', lgnrnd)
        print('datr:', datr)
        # print self.cookies
        for key in self.cookies:
            print(key.name, ':', key.value)
        print('---------------first step end-------------------')

    # get second page
    def login_second_step(self):
        print '---------------second step start----------------'
        sent_url = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'
        request = urllib2.Request(
            url=sent_url, headers=self.headers, data=self.postData)
        content = self.opener.open(request)
        for key in self.cookies:
            print key.name, ':', key.value
        print '---------------second step end------------------'

    # get third page
    def login_third_step(self):
        print '---------------thirt step start-----------------'
        sent_url = 'https://www.facebook.com'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        content = self.opener.open(request)
        # print content.read()
        html = content.read()
        self.account_id = self.get_user_id(html)
        self.async_get_token = self.get_async_get_token(html)
        print '---------------thirt step end------------------'

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

    # get pictrue image
    def get_pictrue_imag(self, html):
        sent_url = HTMLParser.HTMLParser().unescape(html)
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }
        print 'sent_url: ' + sent_url
        request = urllib2.Request(url=sent_url, headers=headers)
        content = self.opener.open(request)
        ContentType = content.headers['Content-Type']
        imgData = base64.b64encode(content.read())
        data_dict = {}
        data_dict['icon_type'] = ContentType
        data_dict['icon'] = imgData
        return data_dict

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
            'nickname': name.encode('utf-8'),
            'url': url.encode('utf-8'),
            'location': area.encode('utf-8')
        }
        avatar = self.get_pictrue_imag(avatar_url)
        formdata = dict(formdata, **avatar)
        self.task.send_data(formdata)
        print '---------------analysis user information end----------------'

    # get user information
    def get_user_information(self):
        try:
            print '--------------get user information start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&id=' + self.id
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            self.analysis_user_information(html)
        except Exception, e:
            traceback.print_exc()
            print e

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
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'friends',
                }
                self.task.send_data(formdata)
        print '---------------analysis user friends end----------------'

    # get user friends
    def get_user_friends(self):
        try:
            print '---------------get user friends start----------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&sk=friends&source_ref=pb_friends_tl&id=' + self.id
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            fb_dtsg_ag = ''
            profile_id = self.id
            __user = self.account_id
            lst = self.get_friends_lst(html)
            pagelet_token = self.get_pagelet_token(html)
            collection_token = self.get_collection_token(html)
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(html)
            else:
                fb_dtsg_ag = self.async_get_token
            cursor = self.get_page_cursor_first(html)
            while True:
                self.analysis_user_friends(html)
                if cursor == '-1' or cursor == 'ARS':
                    break
                # get more friends
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                print 'sent_url : ' + sent_url
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
                cursor = self.get_page_cursor(html)
            print '---------------get user friends end------------------'
        except Exception, e:
            traceback.print_exc()
            print e

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
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'followers',
                }
                self.task.send_data(formdata)
        print '---------------analysis user followers end----------------'

    # get user followers
    def get_user_followers(self):
        try:
            print '--------------get user followers start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&sk=followers&source_ref=pb_friends_tl&id=' + self.id
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            #result = self.analysis_user_followers(html)

            collection_token = self.get_collection_token(html)
            pagelet_token = self.get_pagelet_token(html)
            fb_dtsg_ag = self.get_async_get_token(html)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(html)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(html)
            profile_id = self.id
            cursor = self.get_page_cursor_first(html)
            while True:
                self.analysis_user_followers(html)
                if cursor == '-1' or cursor == 'interaction_boost':
                    break
                # get more friends
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/FollowersAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
                cursor = self.get_page_cursor(html)
            print '---------------get user followers end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

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
                avatar_url = HTMLParser.HTMLParser().unescape(
                    result.group(2).strip())
                name = result.group(3).strip()
                nature = result.group(4).strip()
                user_id = result.group(5).strip()
                formdata = {
                    'index': 'social_platform',
                    'type': 'facebook',
                    'id': user_id,
                    'user_id': user_id,
                    'nature': nature,
                    'nickname': name,
                    'url': url,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'facebook',
                    'id': self.id + '_' + user_id,
                    'source': self.id,
                    'target': user_id,
                    'relation': 'like',
                }
                self.task.send_data(formdata)
        print '---------------analysis user like end----------------'

    # get user likes
    def get_user_likes(self):
        try:
            print '--------------get user likes start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&&sk=likes&id=' + self.id
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            #result = self.analysis_user_likes(html)

            collection_token = self.get_collection_token(html)
            pagelet_token = self.get_pagelet_token(html)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(html)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(html)
            profile_id = self.id
            cursor = self.get_page_cursor_first(html)
            while True:
                self.analysis_user_likes(html)
                if cursor == '-1' or cursor == '277509099012208':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/LikesWithFollowCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
                cursor = self.get_page_cursor(html)
            print '---------------get user likes end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

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
                photo = self.get_pictrue_imag(photo_url)
                formdata = dict(formdata, **photo)
                self.task.send_data(formdata)
        print '---------------analysis user photos end----------------'

    # get user photos
    def get_user_photos(self):
        try:
            print '--------------get user photos start---------------'
            sent_url = 'https://www.facebook.com/profile.php?ref=br_rs&&sk=photos&id=' + self.id
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()

            collection_token = self.get_collection_token(html)
            pagelet_token = self.get_pagelet_token(html)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(html)
            else:
                fb_dtsg_ag = self.async_get_token
            __user = self.account_id
            lst = self.get_friends_lst(html)
            profile_id = self.id
            cursor = self.get_page_cursor_first(html)
            while True:
                self.analysis_user_photos(html)
                if cursor == '-1':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/TaggedPhotosAppCollectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&data={"collection_token":"' + collection_token + '","cursor":"' + cursor + '","disablepager":false,"overview":false,"profile_id":"' + profile_id + '","pagelet_token":"' + pagelet_token + '","tab_key":"friends","lst":"' + lst + '","ftid":null,"order":null,"sk":"friends","importer_state":null}&__user=' + __user + '&__a=1&__req=24&__be=1&__pc=PHASED:DEFAULT&__rev=4357396&__spin_r=4357396&__spin_b=trunk&__spin_t=1538035827'
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
                cursor = self.get_page_cursor(html)
            print '---------------get user photos end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

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
            pattern = re.compile('data-utime="(.*?)".*?<p>(.*?)<', re.S)
            result = re.search(pattern, item)
            if result:
                timestamp = result.group(1)
                remark = result.group(2)
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'facebook',
                    'id': self.id + '_' + timestamp,
                    'user_id': self.id,
                    'nickname': self.name,
                    'timestamp': timestamp.encode('utf-8'),
                    'content': remark.encode('utf-8'),
                }
                self.task.send_data(formdata)
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
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            __user = self.account_id
            ajaxpipe_token = self.get_ajaxpipe_token(html)
            fb_dtsg_ag = ''
            if self.async_get_token == '':
                fb_dtsg_ag = self.get_async_get_token(html)
            else:
                fb_dtsg_ag = self.async_get_token
            data = self.get_data_first(html)
            while True:
                self.analysis_user_timelines(html)
                if data == '-1':
                    break
                sent_url = 'https://www.facebook.com/ajax/pagelet/generic.php/ProfileTimelineSectionPagelet?dpr=1&fb_dtsg_ag=' + fb_dtsg_ag + '&ajaxpipe=1&ajaxpipe_token=' + ajaxpipe_token + '&no_script_path=1&data=' + data + '&__user=' + __user + '&__a=1&__req=fetchstream_4&__be=1&__pc=PHASED:DEFAULT&__rev=4418982&__spin_r=4418982&__spin_b=trunk&__spin_t=1539525330&__adt=4&ajaxpipe_fetch_stream=1'
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
                data = self.get_data(html)
            print '---------------get user timelines end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    def run(self, interval, userid, email, password):
        try:

            self.id = userid
            self.email = email
            self.password = password
            self.login_facebook()

            # sleep for the remaining seconds of interval
            time_remaining = interval - time.time() % interval
            print_ts("Sleeping until %s (%s seconds)..." % (
                (time.ctime(time.time() + time_remaining)), time_remaining))
            time.sleep(time_remaining)

            # get facebook data
            if self.id != '-1':
                # get data
                self.get_user_information()
                self.get_user_friends()
                self.get_user_followers()
                #self.get_user_photos()
                self.get_user_likes()
                self.get_user_timelines()

        except Exception, e:
            traceback.print_exc()
            print e


# facebook data entry

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print 'The parameters are incorrect, please check the parameters.'
        exit()

    # userid = 目标ID
    # email = 爬虫配置账号
    # password = 爬虫配置密码
    # receive_url = 服务器回连地址

    interval = 60
    userid = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    receive_url = sys.argv[4]

    facebook = Facebook(receive_url)
    facebook.run(interval, userid, email, password)
